from django.urls import path
from .views import (  
    ItemDetailView,
    CheckoutView,   
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,

)
from . import views

app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/',OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),    
    path('remove_single_item_from_cart/<slug>/',  remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/', views.category, name='category'),
    path('search/', views.search, name='search'), 

] 