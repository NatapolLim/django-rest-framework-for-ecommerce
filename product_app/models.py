import os
from django.db import models
from django.utils.deconstruct import deconstructible

# Create your models here.

LABEL_CHOICES = (
    ('-', 'Normal'),
    ('S', 'sale'),
    ('N', 'new'),
    ('P', 'promote'),
)
@deconstructible
class GenerateImagePath(object):
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/products/{instance.id}/image'
        name = f'main.{ext}'
        return os.path.join(path,name)

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, blank=True, related_name='category2item')
    label = models.CharField(choices=LABEL_CHOICES, default='-', max_length=1)
    stock_no = models.CharField(max_length=10)
    description_short = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to=GenerateImagePath(), null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('stock_no',), name='unique_stock_no'),
            # models.CheckConstraint(check=models.Q(price__lte=9999), name='price_lte_9999'),
        ]
    def __str__(self) -> str:
        return self.title