from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("apps.users.urls")),
    path("product/", include("apps.products.urls")),
    path("cart/", include("apps.carts.urls")),
    path("order/", include("apps.orders.urls")),
    path("payment/", include("apps.payment.urls")),
]
