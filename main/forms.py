from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "parent", "image"]

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ["name", "slug", "brand",
#                   "category", "country", "description",
#                   "price", "old_price", "discount_percent",
#                   "stock_quantity", "unit", "sku"]

