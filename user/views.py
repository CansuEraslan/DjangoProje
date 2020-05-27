from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from book.models import Category, Comment
from home.models import Setting, UserProfile
from order.models import Order, OrderProduct
from user.forms import UserUpdateForm, ProfileUpdateForm

@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user=request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,'setting':setting,'profile':profile}
    return render(request,'user_profile.html',context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profiliniz güncellendi')
            return redirect('/user')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        user_form = UserUpdateForm(instance=request.user)
        profile_form =ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'setting': setting,
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request,'user_update.html',context)

@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"Pasaportunuz Güncellendi.")
            return HttpResponseRedirect('/user')
        else:
            messages.error(request,'Please correct the error bellow !<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category =Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = PasswordChangeForm(request.user)
        return render(request,'change_password.html',{
            'form':form,
            'category': category,
            'setting': setting,
        })

@login_required(login_url='/login')
def orders(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user=request.user
    orders=Order.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'setting': setting,
        'orders': orders,

    }
    return render(request,'user_orders.html',context)

@login_required(login_url='/login')
def orderdetail(request, id):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'setting': setting,
        'order': order,
        'orderitems': orderitems,

    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    comments = Comment.objects.filter(users_id=current_user.id)
    context = {
        'category': category,
        'setting': setting,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, users_id=current_user.id).delete()
    messages.success(request, 'Yorum silindi')
    return HttpResponseRedirect('/user/comments')