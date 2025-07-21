from django.urls import path, include

# from .views import add_item, remove_item
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from . import tests


# urlpatterns = [path("addItemToCart/", add_item), path("removeItem/", remove_item)]
urlpatterns = [
    path(
        "addItemToCart/<int:cart_id>/",
        views.Add_item_in_cart.as_view(),
        name="Add_item_in_cart",
    ),
    path(
        "removeItemFormCart/<int:item_id>",
        views.Delete_item.as_view(),
        name="Delete_item",
    ),
    path(
        "changeQuantity/<int:item_id>/",
        views.Change_quantity.as_view(),
        name="Change_quantity",
    ),
    # --------------------------
    path("retriveCart/<int:id>", views.Retrive_Cart.as_view(), name="Retrive_Cart"),
    # --------------------------
]

urlpatterns = format_suffix_patterns(urlpatterns)
