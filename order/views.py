from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from book.models import Category
from home.models import Setting
from order.models import ShopCartForm, ShopCart


def index(request):
    return HttpResponse("Order App")

@login_required(login_url='/login')
def addtocart(request,id):
    url=request.META.get('HTTP_REFERER')
    current_user=request.user

    checkproduct=ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control=1
    else:
        control=0
    if request.method=='POST':
        form=ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
                data=ShopCart.objects.get(product_id=id)
                data.quantity+=form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity=form.cleaned_data['quantity']
                data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request,"Ürün başarı ile sepete eklenmiştir.Teşekkür Ederiz")
        return  HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity +=1
            data.save()
        else:
            data=ShopCart()
            data.user_id=current_user.id
            data.product_id=id
            data.quantity=1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request,"Ürün başarı ile sepete eklenmiştir.Teşekkür Ederiz")
        return HttpResponseRedirect(url)
    messages.warning(request,"Ürün sepete eklemede hata oluştu.Lütfen kontrol ediniz")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def shopcart(request):
    category=Category.objects.all()
    current_user=request.user
    setting = Setting.objects.get(pk=1)
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    context={'category':category,
             'shopcart':shopcart,
             'setting':setting,
             }
    return render(request,'Shopcart_products.html',context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    category=Category.objects.all()
    setting = Setting.objects.get(pk=1)
    ShopCart.objects.filter(id=id).delete()
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Ürün sepetten silinmiştir")
    context={'category':category,
             'setting': setting,
             }
    return HttpResponseRedirect("/shopcart")
