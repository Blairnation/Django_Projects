from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cartData, guestOrder
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate

# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    return render(request,'store/store.html', {'products':products, 'cartItems':cartItems})


def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
            
    return render(request, 'store/cart.html', {'items':items, 'order':order, 'cartItems':cartItems})


def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    return render(request, 'store/checkout.html', {'items':items, 'order':order, 'cartItems':cartItems})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if User.objects.filter(username=username):
           messages.error(request, "Username Already Exists!!")
           return redirect('register')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email Already Exists!!")
            return redirect('register')
        
        if password != password2:
            messages.error(request, "Password Doesn't Match!!")
            return redirect('register')
        
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
        customer = Customer.objects.create(user=user,
                                            name=username,
                                            email=email
                                            )
        user.save()
        customer.save()
        messages.success(request, 'Account Registered Successfully')
        return redirect('login')
        
    data = cartData(request)
    cartItems = data['cartItems']

    return render(request, 'store/register.html', {'cartItems':cartItems})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Account Logged In Successfully')
            return redirect('store')
        else:
            messages.error(request, 'Invalid Email Or Password!!')
            return redirect('login')

    data = cartData(request)
    cartItems = data['cartItems']

    return render(request, 'store/login.html', {'cartItems':cartItems})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer= request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product) 
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
       orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item Was Added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
      
    else:
        customer, order = guestOrder(request, data)
       

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()   

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )        

    return JsonResponse('Payment Completed!', safe=False)                             
