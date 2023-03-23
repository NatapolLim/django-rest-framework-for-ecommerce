from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderitem2user', null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(to='product_app.item', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.user.username} | {self.item.title} | {self.quantity}'
    
    def get_total_item_price(self):
        return self.item.price*self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order2user', null=True, blank=True)
    items = models.ManyToManyField(OrderItem,related_name='order2item')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True, blank=True) 
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.id} | {self.user.username}'
    
    def get_total(self):
        total = 0 
        for order_item in self.items.all():
            total+=order_item.get_total_item_price()
        return total
    
# class BillOrder(models.Model):
#     orderitem = models.ForeignKey('transaction_app.OrderItem', on_delete=models.CASCADE, related_name='bill2orderitem')
#     order = models.ForeignKey('transaction_app.Order', on_delete=models.CASCADE, related_name='bill2order')

#     def __str__(self) -> str:
#         return f'{self.id} | {self.order}'