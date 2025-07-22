from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("payWithIframe/", views.PayWithIframe_view.as_view(), name="Pay By IFrame"),
    path("retriveIframCheckoutLink/", views.PayWithIframe_view.as_view()),
    path(
        "stripe_checkout_webhook/",
        views.Stripe_checkout_webhook.as_view(),
        name="Transaction is done",
    ),
    path(
        "stripe_checkout/<int:id>/",
        views.Create_stripe_checkout.as_view(),
        name="stripe-checkout",
    ),
    path(
        "retrieve_stripe_checkout/<str:stripe_checkout_id>/",
        views.Retrieve_stripe_checkout.as_view(),
        name="retrieve-stripe-checkout",
    ),
]


urlpatterns = format_suffix_patterns(urlpatterns)
