from rest_framework.routers import SimpleRouter
from .views import WarehouseViewSet

router = SimpleRouter()

router.register(r"location", WarehouseViewSet)

