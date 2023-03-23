from rest_framework import routers
from .viewsets import CategoryViewSet, ItemViewSet

router = routers.DefaultRouter()

router.register('category', CategoryViewSet)
router.register('item', ItemViewSet)