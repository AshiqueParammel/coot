from django.urls import path,include
from . import views

urlpatterns=[

  
    path('Shop/',views.Shop,name='Shop'),
    path('shop_filter/',views.shop_filter,name='shop_filter'),
    path('shop_sort/',views.shop_sort,name='shop_sort'),
    # path('Quick_view/<int:img_id>',views.Quick_view,name='Quick_view'),
    
    
    
   
]