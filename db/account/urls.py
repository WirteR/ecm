from django.urls import path, include

from .views import RegisterUser, AuthorizeView

urlpatterns = [
    path("register/", RegisterUser.as_view()),
    path("authorize/", AuthorizeView.as_view())
]