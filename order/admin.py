from django.contrib import admin
from .models import item, food_category, order, orderitem

admin.site.register(food_category)
admin.site.register(item)

admin.site.register(order)
admin.site.register(orderitem)