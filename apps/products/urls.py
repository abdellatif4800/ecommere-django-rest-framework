from django.urls import path, include
from .views import Product_management, ProductDetailView, ProductListView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("createProd/", Product_management.as_view()),
    path("updateProd/<int:prod_id>/", Product_management.as_view()),
    path("deleteProd/<int:prod_id>/", Product_management.as_view()),
    # --------- retrive --------------
    path("getProd/<int:id>/", ProductDetailView.as_view()),
    path("getAllProds/", ProductListView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
