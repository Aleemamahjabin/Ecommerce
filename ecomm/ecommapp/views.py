from django.shortcuts import render,redirect
from django.views import View
from ecommapp.forms import UserRegister,LoginForm,CartForm,OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import Product,Cart,Orders
from django.core.mail import send_mail,settings


# Create your views here.
class Home(View):
    def get(self,request):
        data=Product.objects.all()
        return render(request,'index.html',{'products':data})
    
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        product=Product.objects.get(id=id)
        return render(request,'product_detail.html',{'product':product})

class CartView(View):
    def get(self,request,*args,**kwargs):
        form=CartForm()
        product=Product.objects.get(id=kwargs.get('id'))
        return render(request,'addtocart.html',{'form':form,'product':product})

    def post(self,request,*args,**kwargs):
        id=kwargs.get('id')
        user=request.user
        product=Product.objects.get(id=id)
        quantity=request.POST.get('quantity')
        Cart.objects.create(user=user,product=product,quantity=quantity)
        return redirect('home_view')

class CartList(View):
    def get(self,request,*args,**kwargs):
        cart=Cart.objects.filter(user=request.user ).exclude(status='order-placed')
        return render(request,'cartlist.html',{'cart':cart})


class PlaceOrderView(View):
    def get(self,request,*args,**kwargs):
        form=OrderForm()
        return render(request,'placeorder.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        cart_id=kwargs.get('cart_id')
        cart=Cart.objects.get(id=cart_id)
        user=request.user
        address=request.POST.get('address')
        email=request.POST.get('email')
        Orders.objects.create(user=user,cart=cart,address=address,email=email)
        send_mail("confirmation","order placed successfully",settings.EMAIL_HOST_USER,[email])
        cart.status='order-placed'
        cart.save()
        return redirect('home_view')


class CartDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        data=Cart.objects.get(id=id)
        data.delete()
        return redirect('cartlist_view')



class UserRegisterView(View):
    def get(self,request):
        form=UserRegister()
        return render(request,'userreg.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=UserRegister(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Registration successful")
            return redirect('log_form')
            # return HttpResponse('success')
        else:
            messages.error(request,'Invalid')
            return redirect('home_view') 

class Login(View):
    def get(self,request):
        form=LoginForm() 
        return render(request,'login.html',{'form':form})   
     
    def post(self,request,*args,**kwargs):
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=uname,password=pwd)
        if user:
            login(request,user)
            messages.success(request,"Login successful")
            return redirect('home_view')
        else:
            messages.error(request,"Invalid login")
            return redirect('log_form')  

class Logout(View):
    def get(self,request):
        logout(request)
        messages.success(request,'Logout Successful')
        return redirect('home_view')
