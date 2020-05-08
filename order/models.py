from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from book.models import Book


class ShopCart(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Book,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField()

    def __str__(self):
        return self.product

    @property
    def stok(self):
        return (self.product.stok)

class ShopCartForm(ModelForm):
    class Meta:
        model=ShopCart
        fields=['quantity']

