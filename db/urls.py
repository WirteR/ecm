from django.urls import path, include

from .product.urls import router as product_router

urlpatterns = [
    path("product/", include(product_router.urls)),
    path("account/", include("db.account.urls"))
]