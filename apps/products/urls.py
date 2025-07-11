from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("createProduct/", views.Create_product.as_view(), name="Create Product"),
    path(
        "updateProduct/<int:id>/",
        views.Update_product.as_view(),
        name="Update Product",
    ),
    path(
        "deleteProduct/<int:id>/",
        views.Delete_product.as_view(),
        name="Delete Product",
    ),
    # --------- manage images --------------
    path(
        "addNewImage/",
        views.AddNewImage.as_view(),
        name="add new image for existed prod",
    ),
    path(
        "updateImage/<int:id>/",
        views.UpdateNewImage.as_view(),
        name="udate existed image",
    ),
    # --------- retrive products --------------
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
