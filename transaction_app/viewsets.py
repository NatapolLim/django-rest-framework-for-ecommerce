from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import OrderItem, Order
from .serializers import OrderItemSerializer, OrderSerializer
from .permissions import IsMember, IsOwnerOrder
from django.db.models import Q

class OrderItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsMember,]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsMember, IsOwnerOrder]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super(OrderViewSet, self).get_queryset()

        filter_queryset = queryset.filter(user=user)
        return filter_queryset
    
    @action(detail=True, methods=['post'], name='Remove Item')
    def remove_item(self, request, pk=None):
        try:
            order = self.get_object()
            user = request.user
            # if order.user!=user:
            #     print('+++++++++ notmatchuser')
            #     return Response({'detail':'User is not belong to this Order'},
            #                     status=status.HTTP_400_BAD_REQUEST)
            item_id = request.data.get('item_id',None)
            if item_id==None:
                return Response({'detail':'Please provide item_id in order to delete from Order'},
                                status=status.HTTP_400_BAD_REQUEST)
            
            orderitem = OrderItem.objects.get(Q(user=user) & Q(item__id=item_id))
            # if len(orderitem)==0:
            #     return Response({'detail':f'Have no item that belong to user_id :{user.id}'},
            #                     status=status.HTTP_400_BAD_REQUEST)
            order.items.remove(orderitem)
            order.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'detail':'Have no orderitem that belong to user'},
                            status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], name='Add Item')
    def add_item(self,request, pk=None):
        try:
            order = self.get_object()
            user = request.user
            item_id = request.data.get('item_id',None)
            if item_id==None:
                return Response({'detail':'Please provide item_id in order to delete from Order'},
                                status=status.HTTP_400_BAD_REQUEST)
            
            orderitem = OrderItem.objects.get(Q(user=user) & Q(item__id=item_id))
            order.items.add(orderitem)
            order.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'detail':'Have no orderitem that belong to user'},
                            status=status.HTTP_400_BAD_REQUEST)



        
        
        
        


