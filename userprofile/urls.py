from django.urls import path
from . import views

urlpatterns=[

  
    path('userprofile',views.userprofile,name='userprofile'),
 
    path('add_address/<int:add_id>',views.add_address,name='add_address'),
    path('edit_address/<int:edit_id>',views.edit_address,name='edit_address'),
    path('View_address/<int:view_id>',views.View_address,name='View_address'),
    path('delete_address/<int:delete_id>',views.delete_address,name='delete_address'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('order_view_user/<int:view_id>',views.order_view_user,name='order_view_user'),
  

    
   
]