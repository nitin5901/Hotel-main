from django import forms
from .models import  item, food_category


class ItemForm(forms.ModelForm):
    class Meta:
        model = item
        fields = ('name', 'category', 'price' )
