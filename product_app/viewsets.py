from rest_framework import viewsets, mixins

from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer
from .permissions import IsMember

class CategoryViewSet(viewsets.ModelViewSet):

    permission_classes = [IsMember,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  ):
    
    permission_classes = [IsMember,]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
