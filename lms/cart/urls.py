from django.urls import path, include
from . import views

urlpatterns = [
    path('add-to-cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:course_id>/', views.remove_from_cart, name='remove_from_cart'),
    #path('cart/', views.cart, name='cart'),
    path('', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment_confirmation, name='payment')
    #path('/payment/', views., name='payment')
]