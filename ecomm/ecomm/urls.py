"""
URL configuration for ecomm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecommapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(),name='home_view'),
    path('userreg', views.UserRegisterView.as_view(),name='user_reg'),
    path('login', views.Login.as_view(),name='log_form'),
    path('logout', views.Logout.as_view(),name='logout'),
    path('product/detail/<int:id>', views.ProductDetailView.as_view(),name='detail_view'),
    path('cart/<int:id>', views.CartView.as_view(),name='cart_view'),
    path('cart/list', views.CartList.as_view(),name='cartlist_view'),
    path('place/order/<int:cart_id>', views.PlaceOrderView.as_view(),name='place_order'),
    path('cart/delete/<int:id>', views.CartDeleteView.as_view(),name='cart_delete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
