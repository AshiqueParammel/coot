from django.urls import path
from . import views

urlpatterns=[
    
    path('cart<int:prod_id>',views.cart,name='cart'),
    path('remove_cart<int:prod_id>',views.remove_cart,name='remove_cart'),
      
]