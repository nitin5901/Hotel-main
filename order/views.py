from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import item, food_category, orderitem, order
from .forms import ItemForm
from home.models import person

from django.views.decorators.csrf import csrf_exempt
#from paytm.payments import PaytmPaymentPage
#from paytm.payments import VerifyPaytmResponse,JsonResponse
from .Paytm import Checksum
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'lE6YN@L!%4GBKg%I'


def index(request):
    all_cat = food_category.objects.all()
    list1 = []
    list2 = []
    i=1
    for cat  in all_cat:
        if i<6:
            li = item.objects.filter(category=cat)
            list1.append(li)
            i = i+1
        else:
            li = item.objects.filter(category=cat)
            list2.append(li)
    return render(request, 'order/index.html', {'list1':list1, 'list2':list2 })


def item_form(request):
    categorys = food_category.objects.all()
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save(True)
            return redirect('order:index')
        else:
            return HttpResponse("Nhi hua")
    return render(request, 'order/item_form.html', {'categorys':categorys })


def item_edit(request,pk):
    itm = item.objects.get(pk=pk)
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        itm.name = name
        itm.price = price
        itm.save()
        return redirect('order:item-list')
    return render(request, 'order/item_edit_form.html', {'item':itm })


def item_delete(request,pk):
    itm = item.objects.get(pk=pk)
    itm.delete()
    categorys = food_category.objects.all()
    items = []
    for cat in categorys:
        its = item.objects.filter(category=cat)
        for it in its:
            items.append(it)
    return render(request, 'order/item_list.html', {'items':items })


def item_list(request):
    categorys = food_category.objects.all()
    items = []
    for cat in categorys:
        its = item.objects.filter(category=cat)
        for it in its:
            items.append(it)
    return render(request, 'order/item_list.html', {'items':items })


def add_to_cart(request, pk):
    if request.user.is_authenticated:
        it = item.objects.get(pk=pk)
        prsn = person.objects.get(user=request.user)
        if order.objects.filter(user=prsn, completed=False).count() >0:
            oder = order.objects.get(user=prsn, completed=False)
        else:
            oder = order(user=prsn)
            oder.save()
        if orderitem.objects.filter(order=oder,item=it).count() >0:
            oi = orderitem.objects.get(order=oder,item=it)
            oi.quantity = oi.quantity + 1
        else:
            oi = orderitem(item=it, order=oder, quantity=1)
        oi.save()
        return redirect('order:index')
    return HttpResponse("Please Login to add items. ")


def plus_to_cart(request, pk):
    if request.user.is_authenticated:
        oi = orderitem.objects.get(pk=pk)
        oi.quantity = oi.quantity + 1
        oi.save()
        return redirect('order:cart-view')
    return HttpResponse("Please Login to add items. ")


def minus_to_cart(request, pk):
    if request.user.is_authenticated:
        oi = orderitem.objects.get(pk=pk)
        oi.quantity = oi.quantity - 1
        oi.save()
        if oi.quantity == 0 :
            oi.delete()
        return redirect('order:cart-view')
    return HttpResponse("Please Login to add items. ")



def cart_view(request):
    if request.user.is_authenticated:
        prsn = person.objects.get(user=request.user)
        if order.objects.filter(user=prsn, completed=False).count() >0:
            oder = order.objects.get(user=prsn, completed=False)
            items = orderitem.objects.filter(order=oder)
            totals=[]
            g_total = 0
            for itm in items:
                tot = int(itm.item.price) * int(itm.quantity)
                g_total = g_total + tot
                totals.append(tot)
            oder.total = g_total
            oder.save()
        else:
            return HttpResponse("Cart is Empty. ")
        xyz = zip(items, totals)
        return render(request, 'order/cart.html', {'prsn':prsn, 'items':xyz, 'g_total':g_total  })
    return HttpResponse("Please Login to view Cart. ")


def checkout(request):
    if request.user.is_authenticated:
        prsn = person.objects.get(user=request.user)
        if order.objects.filter(user=prsn, completed=False).count() >0:
            oder = order.objects.get(user=prsn, completed=False)
            param_dict = {
                'MID': 'ADdYJP68142813746242',
                'ORDER_ID': str(oder.id),
                'TXN_AMOUNT': str(oder.total),
                'CUST_ID': str(oder.user.id) ,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://navdurga.pythonanywhere.com/menu/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'order/paytm.html', {'param_dict': param_dict})
        else:
            return HttpResponse("Cart is Empty. ")
        return render(request, 'order/cart.html', {'prsn':prsn, 'order':oder   })
    return HttpResponse("Please Login to view Cart. ")


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            opk = response_dict['ORDERID']
            oder = order.objects.get(pk=opk)
            oder.completed = True
            oder.save()
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'order/paymentstatus.html', {'response': response_dict})
