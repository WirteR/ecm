from rest_framework.routers import SimpleRouter
from db.service import views as service_views

router = SimpleRouter()

router.register(r"logs/purchaseorder", service_views.PurchaseOrderLogViewSet)
router.register(r"logs/saleorder", service_views.SellOrderLogView)
router.register(r"trash/products", service_views.ProductTrashViewSet)
router.register(r"trash/categories", service_views.CategoriesTrashViewSet)
router.register(r"trash/inventory", service_views.InventoryTrashViewSet)
router.register(r"trash/purchaseorders", service_views.PurchaseOrderTrashViewSet)
router.register(r"trash/sellorders", service_views.SellOrderTrashViewSet)
router.register(r"trash/payments", service_views.PaymentTrashViewSet)
router.register(r"trash/expenses", service_views.ExpenseTrashViewSet)