from rest_framework import routers
from .viewsets import OrderItemViewSet, OrderViewSet

router = routers.DefaultRouter()

router.register('orderitem' ,OrderItemViewSet)
router.register('order' ,OrderViewSet)