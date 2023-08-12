from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [

    path("", views.index, name='index'),
    path("add/", views.item_form, name='item-add'),
    path("edit/<int:pk>", views.item_edit, name='item-edit'),
    path("delete/<int:pk>", views.item_delete, name='item-del'),
    path("list/", views.item_list, name='item-list'),

    path("cart/add/<int:pk>", views.add_to_cart, name='cart-add'),
    path("cart/plus/<int:pk>", views.plus_to_cart, name='cart-plus'),
    path("cart/minus/<int:pk>", views.minus_to_cart, name='cart-minus'),

    path("cart/", views.cart_view , name='cart-view'),
    path("checkout/", views.checkout, name="checkout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    #path("bill/", views.bill_view , name='bill-view'),

]

