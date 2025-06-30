from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("createProduct/", views.Create_product.as_view(), name="Create Product"),
    path(
        "updateProduct/<int:prod_id>/",
        views.Update_product.as_view(),
        name="Update Product",
    ),
    path(
        "deleteProduct/<int:prod_id>/",
        views.Delete_product.as_view(),
        name="Delete Product",
    ),
    # --------- retrive --------------
    path(
        "productByID/<int:prod_id>/",
        views.Product_by_id.as_view(),
        name="Product by id",
    ),
    path(
        "productsByCategories/<str:category>/",
        views.CategoriesListView.as_view(),
        name="by categories",
    ),
]


# urlpatterns = format_suffix_patterns(urlpatterns)
