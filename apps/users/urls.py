from django.urls import path, include
from .views import UserRegiester, Signin
from rest_framework.urlpatterns import format_suffix_patterns
from . import tests

urlpatterns = [
    path("register/", UserRegiester.as_view(), name="signup"),
    path("signin/", Signin.as_view(), name="signin"),
]


# urlpatterns = format_suffix_patterns(urlpatterns)
