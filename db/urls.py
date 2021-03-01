from django.urls import path, include

from .product.urls import router as product_router
from .orders.urls import router as order_router
from .warehouse.urls import router as warehouse_router

urlpatterns = [
    path("product/", include(product_router.urls)),
    path("order/", include(order_router.urls)),
    path("account/", include("db.account.urls")),
    path("warehouse/", include(warehouse_router.urls))
]