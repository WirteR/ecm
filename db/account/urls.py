from django.urls import path, include

from .views import RegisterUser, RegisterSuperUser, AuthorizeView

urlpatterns = [
    path("register/", RegisterUser.as_view()),
    path("register-admin/", RegisterSuperUser.as_view()),
    path("authorize/", AuthorizeView.as_view())
]