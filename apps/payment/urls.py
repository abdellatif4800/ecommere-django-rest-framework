from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("payWithIframe/", views.PayWithIframe_view.as_view(), name="Pay By IFrame"),
    path("retriveIframCheckoutLink/", views.PayWithIframe_view.as_view()),
    path("transactionCheck/", views.Transaction_view.as_view(),
         name="Transaction is done")
]


urlpatterns = format_suffix_patterns(urlpatterns)
