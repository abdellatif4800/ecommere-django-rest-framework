from django.urls import path, include
from .views import UserRegiester, Signin
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("register/", UserRegiester.as_view()),
    path("signin/", Signin.as_view()),
]


# urlpatterns = format_suffix_patterns(urlpatterns)
