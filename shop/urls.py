from django.urls import path,include
from . import views

urlpatterns=[

  
    path('Shop/',views.Shop,name='Shop'),
    # path('Quick_view/<int:img_id>',views.Quick_view,name='Quick_view'),
    
    
    
   
]