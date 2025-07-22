import requests
import json
import os
from apps.products import serializer
from dotenv import load_dotenv
from pprint import pprint
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .helper import gen_token
from .models import Transaction, Init_payment, Stripe_checkout
from .serializer import (
    Init_paymentSerializer,
    Transaction_serialiazer,
    Stripe_checkout_serializer,
)
from apps.orders.models import Order, OrderItem
from apps.products import models as prod_models
import stripe
from datetime import datetime
from django.utils import timezone
from rest_framework import status

# -----------------
load_dotenv()

paymob_secret_key = os.getenv("PAYMOB_SECRET_KEY")
payment_by_card_intgration_id = os.getenv("PAYMENT_BY_CARD_INTEGRATION_ID")
ifram_key = os.getenv("IFRAME_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# -----------------


class PayWithIframe_view(APIView):
    def post(self, request):
        url = "https://accept.paymob.com/v1/intention/"

        payload = {
            "amount": request.data.get("amount"),
            "currency": request.data.get("currency", "EGP"),
            "billing_data": request.data.get("billing_data"),
            "payment_methods": [int(payment_by_card_intgration_id)],
            "expiration": 3600,  # in 1 hour
        }

        headers = {
            "Authorization": f"Token {paymob_secret_key} ",
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        payment_key = response.json()["payment_keys"][0]["key"]

        # ******************************************#

        if response.json().get("status") == "intended":
            print(response.json())
            data = {
                "order": request.data["order_id"],
                "api_source": Init_payment.IFRAME,
                "payment_link_id": response.json().get("id"),
                "checkout_link": f"https://accept.paymob.com/api/acceptance/iframes/{int(ifram_key)}?payment_token={payment_key}",
                "amount_cents": response.json()["intention_detail"]["amount"],
                "paymob_order_id": int(response.json()["payment_keys"][0]["order_id"]),
            }

            serializer = Init_paymentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "checkout url": f"https://accept.paymob.com/api/acceptance/iframes/{int(ifram_key)}?payment_token={payment_key}",
                        "db res": serializer.data,
                    }
                )
            else:
                return Response({"db error": serializer.errors})

        # return Response({
        # "checkout url": f"https://accept.paymob.com/api/acceptance/iframes/{int(ifram_key)}?payment_token={payment_key}"
        # })
        # ******************************************#

    def get(self, request):
        order_id = int(request.query_params.get("order_id"))

        target_payment = Init_payment.objects.filter(order=order_id).first()
        return Response(Init_paymentSerializer(target_payment).data)


# class Paymob_webhook(generics.CreateAPIView):
#     serializer_class = Transaction_serialiazer
#     queryset = Transaction.objects.all()

#     def post(self, request):
#         # if request.data["obj"]["success"] == True:
#         #     # change state in init_payment
#         #     init_payment = Init_payment.objects.get(
#         #         paymob_order_id=request.data["obj"]["order"]["id"]
#         #     )
#         #     # paymob_order_id=329355537)

#         #     init_payment.status = "PAID"
#         #     init_payment.save()
#         #     # ******************************************#
#         #     # change order state in db
#         #     init_payment.order.shipping_status = Order.PROCESSING
#         #     init_payment.order.save()
#         #     # ******************************************#
#         #     # save transaction in db
#         #     Transaction.objects.create(
#         #         transction_id=request.data["obj"]["id"],
#         #         paymob_order_id=request.data["obj"]["order"]["id"],
#         #         amount_cents=request.data["obj"]["order"]["amount_cents"],
#         #         success=request.data["obj"]["success"],
#         #         api_source=request.data["obj"]["api_source"],
#         #         created_at=request.data["obj"]["created_at"],
#         #         order=Order.objects.get(id=init_payment.order.id),
#         #     )
#         #     # ******************************************#
#         #     print("transction completed")
#         #     return Response("transction completed")
#         # else:
#         #     print("transction filed")
#         #     return Response("transction filed")
#         # # return Response(init_payment.order.shipping_status)


class Create_stripe_checkout(generics.CreateAPIView):
    serializer_class = Stripe_checkout_serializer
    queryset = Stripe_checkout.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["id"])
        order_items = get_list_or_404(OrderItem, order=kwargs["id"])

        items = []

        for item in order_items:
            target_product = get_object_or_404(prod_models.Product, id=item.product.id)

            if target_product.stripe_price_id is None:
                stripe_price = stripe.Price.create(
                    currency="usd",
                    unit_amount=target_product.price,
                    product_data={"name": target_product.name},
                )

                if stripe_price is not None:
                    target_product.stripe_price_id = stripe_price.id
                    target_product.save()
                    items.append(
                        {
                            "price": target_product.stripe_price_id,
                            "quantity": item.quantity,
                        }
                    )
            else:
                retrieve_price = stripe.Price.retrieve(target_product.stripe_price_id)
                items.append({"price": retrieve_price, "quantity": item.quantity})

        checkout = stripe.checkout.Session.create(
            success_url="http://example.com/success",
            line_items=items,
            mode="payment",
        )

        expiration = timezone.make_aware(datetime.fromtimestamp(checkout.expires_at))

        data = {
            "order": order.id,
            "payment_link": checkout.url,
            "amount": checkout.amount_total,
            "stripe_checkout_id": checkout.id,
            "has_paid": False,
            "expiration": expiration,
            "success_url": checkout.success_url,
        }

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Retrieve_stripe_checkout(generics.RetrieveAPIView):
    serializer_class = Stripe_checkout_serializer
    queryset = Stripe_checkout.objects.all()
    lookup_field = "stripe_checkout_id"

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if timezone.now() > instance.expiration:
            return Response(
                f"link expired {instance.expiration}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)


class Stripe_checkout_webhook(generics.UpdateAPIView):
    serializer_class = Stripe_checkout_serializer
    # lookup_field = "stripe_checkout_id"
    queryset = Stripe_checkout.objects.all()

    def get_object(self):
        checkout_id = self.request.data.get("data").get("object").get("id")
        return Stripe_checkout.objects.get(stripe_checkout_id=checkout_id)

    def post(self, request):
        if request.data.get("data").get("object").get("status") == "complete":
            checkout = self.get_object()
            checkout.has_paid = True
            checkout.save()
            return Response("payment is successed", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("payment is faild", status=status.HTTP_402_PAYMENT_REQUIRED)


# print(
# webhook_endpoints = stripe.WebhookEndpoint.modify(
#     "we_1RiqGSH05IPbx08PEpIX6dHU",
#     enabled_events=["checkout.session.completed"],
#     url="https://connections-precipitation-circle-come.trycloudflare.com/payment/stripe_checkout_webhook/",
# )
# )

# print(
#  stripe.WebhookEndpoint.create(
#     enabled_events=["checkout.session.completed"],
#     url="https://connections-precipitation-circle-come.trycloudflare.com/payment/stripe_checkout_webhook/",
# )
# )

# print(stripe.WebhookEndpoint.list())
# print(stripe.Event.list())
