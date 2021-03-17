from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import RegisterAdmin, AuthorizeAdmin, SuperuserGroupViewset

router = SimpleRouter()

router.register(r"groups", SuperuserGroupViewset)


urlpatterns = [
    path("register/", RegisterAdmin.as_view()),
    path("authorize/", AuthorizeAdmin.as_view()),
    path("", include(router.urls))
]