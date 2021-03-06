import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from book.models import Category, Book, Images, Comment

from home.forms import SearchForm, SignUpForm

from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ
from order.models import ShopCart


def index(request):
    setting=Setting.objects.get(pk=1)
    sliderdata = Book.objects.all()[:4]
    category = Category.objects.all()
    dayproduct=Book.objects.all()[:3]
    lastproduct = Book.objects.all().order_by('-id')[:3]
    randomproduct = Book.objects.all().order_by('?')[:3]
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    context={'setting':setting,
             'category': category,
             'sliderdata':sliderdata,
             'page':'home',
             'dayproduct':dayproduct,
             'lastproduct':lastproduct,
             'randomproduct':randomproduct,
             }
    return render(request, 'index.html', context)



def hakkimizda(request):
    setting=Setting.objects.get(pk=1)
    category = Category.objects.all()

    context={'setting':setting,
             'page':'hakkimizda',
             'category':category,
            }
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting=Setting.objects.get(pk=1)
    category = Category.objects.all()

    context={'setting':setting,
             'category':category,
            }
    return render(request, 'referanslar.html', context)


def kitaplar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    products = Book.objects.all()
    context = {
        'setting': setting,
        'products':products,
        'category': category,

    }
    return render(request, 'booksmenu.html', context)


def iletisim(request):
    if request.method=='POST':
        form=ContactFormu(request.POST)
        if form.is_valid():
            data=ContactFormMessage()
            data.name=form.cleaned_data['name']
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Mesajınız Gönderilmiştir")
            return  HttpResponseRedirect('/iletisim')
    setting=Setting.objects.get(pk=1)
    form=ContactFormu()
    category = Category.objects.all()

    context={'setting':setting,'form':form,'category':category,}
    return render(request, 'iletisim.html', context)


def category_products(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products=Book.objects.filter(category_id=id)
    context={'products':products,
             'setting': setting,
             'category':category,
             'categorydata':categorydata,
             }
    return render(request, 'books.html', context)


def product_detail(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Book.objects.get(pk=id)
    images = Images.objects.filter(book_id=id)
    comments=Comment.objects.filter(product_id=id,status='True')
    context = {'product':product,
               'category': category,
               'images':images,
               'setting': setting,
               'comments':comments,
               }
    return render(request, 'product_detail.html',context)


def product_search(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            category=Category.objects.all()
            setting = Setting.objects.get(pk=1)
            query=form.cleaned_data['query']
            catid=form.cleaned_data['catid']
            if catid==0:
                products=Book.objects.filter(title__icontains=query)
            else:
                products = Book.objects.filter(title__icontains=query,category_id=catid)
            context = {'products': products,
                       'category': category,
                       'setting':setting,
                       }
            return render(request, 'product_search.html', context)
    return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q=request.GET.get('term','')
        product=Book.objects.filter(title__icontains=q)
        results=[]
        for rs in product:
            product_json={}
            product_json=rs.title
            results.append(product_json)
        data=json.dumps(results)
    else:
        data='fail'
    mimetype='application/json'
    return HttpResponse(data,mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user=request.user
            userprofile=UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage']=userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası !  Kullanıcı adı veya şifre yanlış. ")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category': category,'setting':setting,}
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user=request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request, "Üye olma işleminiz başarı ile gerçekleştirildi.")
            return HttpResponseRedirect('/')
    form = SignUpForm()
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category': category,'form':form, 'setting': setting, }
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    faq=FAQ.objects.all().order_by('ordernumber')
    context={'category':category,
             'setting':setting,
             'faq':faq,

             }
    return render(request,'faq.html',context)