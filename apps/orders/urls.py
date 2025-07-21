from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path(
        "newOrder/fromCart/<int:cart_id>/",
        views.Create_order.as_view(),
        name="new-order",
    ),
    path(
        "getOrderByID/<int:id>/",
        views.Retrive_order.as_view(),
        name="retrive_order",
    ),
]
