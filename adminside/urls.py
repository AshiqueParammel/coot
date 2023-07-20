from django.urls import path
from . import views

urlpatterns=[

  
    path('admin_signup',views.admin_signup,name='admin_signup'),
    path('usermanagement_1',views.usermanagement_1,name='usermanagement_1'),
    path('admin_login1',views.admin_login1,name='admin_login1'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('admin_forgotpassword',views.admin_forgotpassword,name='admin_forgotpassword'),
    path('admin_logout1',views.admin_logout1,name='admin_logout1'),
    path('blockuser/<int:user_id>',views.blockuser,name='blockuser'),
    path('user_view/<int:user_id>',views.user_view,name='user_view'),
   
    
   
    
     
]