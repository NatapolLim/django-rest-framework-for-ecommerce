from rest_framework import serializers

# from django.contrib.auth.models import User
from.models import OrderItem, Order
from product_app.models import Item
from datetime import datetime
from django.utils import timezone
from django.db.models import Q

class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='user-detail')
    order2item = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='order-detail')
    item = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='item-detail')
    class Meta:
        model = OrderItem
        fields = ['url', 'id', 'user', 'ordered', 'item', 'quantity', 'order2item', ]
    
    def validate_quantity(self, value):
        if value>100:
            raise serializers.ValidationError('Quantity can not moer than 100')
        return value
    
    def create(self, validated_date):
        user = self.context['request'].user
        orderitem = OrderItem.objects.create(**validated_date)
        orderitem.user=user
        orderitem.save()
        return orderitem

class OrderSerializer(serializers.ModelSerializer):
    OrderItems = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='orderitem-detail', source='items')
    amount = serializers.IntegerField(source='get_total', read_only=True)
    class Meta:
        model = Order
        fields = ['url', 'id', 'user', 'start_date', 'ordered_date', 'ordered',
                  'being_delivered', 'received', 'amount', 'OrderItems']
        
    def validate(self, attrs):
        method = self.context['request'].method
        if method=='POST':
            user = self.context['request'].user

            if 'items' in attrs:
                items = attrs['items']
                for item in items:
                    if item.user!=user:
                        raise serializers.ValidationError('OrderItem not belong to User') 
            value = self.context['request'].data.get('items', None)
            if value==None:
                raise serializers.ValidationError('OrderItem is None') 
            items = OrderItem.objects.filter(Q(user=user) & Q(item__id=value))
            if len(items)==0:
                raise serializers.ValidationError('OrderItem not belong to User')
            return attrs
    
    def create(self, validated_date,):
        user = self.context['request'].user

        # all_order_items = OrderItem.objects.get_queryset()
        # filter_items = all_order_items.filter(user = user)
        value = self.context['request'].data.get('items', None)
        items = OrderItem.objects.filter(Q(user=user) & Q(item__id=value))
        order = Order.objects.create(**validated_date)
        order.user=user
        order.ordered_date=timezone.now()
        order.save()
        order.items.set(items)
        order.save()
        return order
