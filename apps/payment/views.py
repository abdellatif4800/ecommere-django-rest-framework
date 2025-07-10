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
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .helper import gen_token
from .models import Transaction, Init_payment
from .serializer import Init_paymentSerializer, TransactionSerialiazer
from apps.orders.models import Order
import stripe

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


class Transaction_view(APIView):
    def post(self, request):
        pprint(dict(request.data))
        return Response(123)
        # if request.data["obj"]["success"] == True:
        #     # change state in init_payment
        #     init_payment = Init_payment.objects.get(
        #         paymob_order_id=request.data["obj"]["order"]["id"]
        #     )
        #     # paymob_order_id=329355537)

        #     init_payment.status = "PAID"
        #     init_payment.save()
        #     # ******************************************#
        #     # change order state in db
        #     init_payment.order.shipping_status = Order.PROCESSING
        #     init_payment.order.save()
        #     # ******************************************#
        #     # save transaction in db
        #     Transaction.objects.create(
        #         transction_id=request.data["obj"]["id"],
        #         paymob_order_id=request.data["obj"]["order"]["id"],
        #         amount_cents=request.data["obj"]["order"]["amount_cents"],
        #         success=request.data["obj"]["success"],
        #         api_source=request.data["obj"]["api_source"],
        #         created_at=request.data["obj"]["created_at"],
        #         order=Order.objects.get(id=init_payment.order.id),
        #     )
        #     # ******************************************#
        #     print("transction completed")
        #     return Response("transction completed")
        # else:
        #     print("transction filed")
        #     return Response("transction filed")
        # # return Response(init_payment.order.shipping_status)


# webhook_endpoint = stripe.WebhookEndpoint.create(
#     enabled_events=["charge.succeeded", "charge.failed"],
#     url="https://magical-betting-las-maple.trycloudflare.com/payment/transactionCheck/",
# )
# webhook_endpoints = stripe.WebhookEndpoint.list(limit=3)


# session = stripe.checkout.Session.create(
#     success_url="https://magical-betting-las-maple.trycloudflare.com/payment/transactionCheck/",
#     line_items=[{"price": "price_1RipSRH05IPbx08PlfDVWP9V", "quantity": 2}],
#     mode="payment",
# )

# print(session)

# price = stripe.Price.create(
#     currency="usd",
#     unit_amount=1000,
#     product_data={"name": "prod101"},
# )
# print(price)

# prices = stripe.Price.list()
# print(prices)

# payment_link = stripe.PaymentLink.create(
# line_items=[{"price": "price_1RipSRH05IPbx08PlfDVWP9V", "quantity": 1}],
# )
# print(payment_link)
