from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def INDEX(request):
    main_category = MainCategory.objects.all()
    product = Product.objects.filter(section__name = 'Top Deal of the Day')
    context ={
        'main_category':main_category,
        'products':product
    }
    return render(request,'user/index.html',context)

def PRDUCTDETAIL(request,slug):
    products = Product.objects.filter(slug = slug)
    if products.exists():
        products = Product.objects.filter(slug = slug)
    else:
        return redirect('error404')
    context ={
            'products':products
    }
    return render(request,'user/product_detail.html',context)

def ERROR404(request):
    return render(request,'common/404.html')

def MYACCOUNT(request):
    return render(request,'registeration/login.html')

def REGISTER(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        if User.objects.filter(username=username).exists():
            messages.error(request,'username is already exists')
            return redirect ('login')   
        if User.objects.filter(email=email).exists():
            messages.error(request,'Sorry email already exists')
            return redirect ('login') 
        else:
            if password==confirm_password:
             user = User(username=username,email= email)
             user.set_password(password)
             user.save()
             messages.success(request,'Account Created Sucessfully')
            else:
                messages.error(request,'Password not Matched')
    return redirect('myaccount')

def LOGIN(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Sucessfully')
            return redirect('homepage')
        else:
            messages.error(request,'Invalid Credentials!!')
            return redirect('myaccount')
    return render(request,'registeration/login.html')

@login_required(login_url='login')
def PROFILE(request):
    return render(request,'user/profile.html')


@login_required(login_url='login')
def PROFILEUPDATE(request):
    if request.method == 'POST':
        username= request.POST.get('user_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('user_password')
        user_id = request.user.id
        
        user = User.objects.get(id=user_id)
        user.first_name=first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        
        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,"Profile Updated Sucessfully")
    return redirect('profile')

def ABOUTUS(request):
    return render(request,'user/about.html')

def CONTACTUS(request):
    return render(request,'user/contact.html')

def PRODUCTLIST(request):
    category = Category.objects.all()
    product = Product.objects.all()
    context ={
        'category':category,
        'product':product
    }
    return render(request,'user/product.html',context)

def FILTER_DATA(request):
     categories = request.GET.getlist('category[]')
     brands = request.GET.getlist('brand[]')
     allProducts = Product.objects.all().order_by('-id').distinct()
     if len(categories) > 0:
         allProducts = allProducts.filter(categories__id__in=categories).distinct()
     if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()
     t = render_to_string('Ajax/product-filtered-list.html', {'product': allProducts})
     return JsonResponse({'data': t})















def LOGOUT(request):
    logout(request)
    return redirect ("/")