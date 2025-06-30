from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

#     openapi.Info(
#         title="Ecommerce DRF API",
#         default_version="v1",
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@snippets.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # ------------------------------------
    # path(
    #     "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    # ),
    # path(
    #     "swagger/",
    #     schema_view.with_ui("swagger", cache_timeout=0),
    #     name="schema-swagger-ui",
    # ),
    # path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # ------------------------------------
    path("admin/", admin.site.urls),
    # ------------------------------------
    # path("auth/", include("apps.users.urls")),
    path("product/", include("apps.products.urls")),
    # path("cart/", include("apps.carts.urls")),
    # path("order/", include("apps.orders.urls")),
    # path("payment/", include("apps.payment.urls")),
]
