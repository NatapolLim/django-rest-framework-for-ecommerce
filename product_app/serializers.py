from rest_framework import serializers

from .models import Category, Item

class CategorySerializer(serializers.ModelSerializer):
    itemlists = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='item-detail', source='category2item')
    class Meta:
        model = Category
        fields = ['url', 'id', 'title' ,'description', 'is_active', 'itemlists']


class ItemSerializer(serializers.ModelSerializer):
    category_url = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='category-detail', source='category')
    
    class Meta:
        model = Item
        fields = ['url', 'id', 'title', 'price', 'discount_price',
                  'category', 'category_url', 'label', 'stock_no', 'description_short',
                  'description' ,'image', 'is_active']
        
    # def validate_stock_no(self, data):
    #     all_stock_no = Item.objects.get_queryset()
    #     print(all_stock_no)
        
    #     return data