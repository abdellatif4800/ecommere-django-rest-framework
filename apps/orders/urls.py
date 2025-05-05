from django.urls import path, include
from .views import Order_view, OrderList_view
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("getOrderList/", OrderList_view.as_view()),
    path("addOrder/", Order_view.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
