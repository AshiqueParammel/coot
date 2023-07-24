from django.urls import path,include
from . import views

urlpatterns=[

  
    path('',views.home,name='home'),
      path('product_show/<int:prod_id>/<int:img_id>',views.product_show,name='product_show'),
    
   
]