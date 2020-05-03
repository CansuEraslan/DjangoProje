from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from book.models import Category, Book
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    setting=Setting.objects.get(pk=1)
    sliderdata = Book.objects.all()[:4]
    category = Category.objects.all()
    dayproduct=Book.objects.all()[:3]
    lastproduct = Book.objects.all().order_by('-id')[:3]
    randomproduct = Book.objects.all().order_by('?')[:3]
    context={'setting':setting,
             'category': category,
             'sliderdata':sliderdata,
             'page':'home',
             'dayproduct':dayproduct,
             'lastproduct':lastproduct,
             'randomproduct':randomproduct,}
    return render(request, 'index.html', context)
def hakkimizda(request):
    setting=Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={'setting':setting,
             'page':'hakkimizda',
             'category':category}
    return render(request, 'hakkimizda.html', context)
def referanslar(request):
    setting=Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={'setting':setting,
             'category':category}
    return render(request, 'referanslar.html', context)
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
    context={'setting':setting,'form':form,'category':category}
    return render(request, 'iletisim.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products=Book.objects.filter(category_id=id)
    context={'products':products,
             'category':category,
             'categorydata':categorydata
             }
    return render(request, 'books.html', context)