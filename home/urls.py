from django.urls import path,include
from . import views

urlpatterns=[

  
  path('',views.home,name='home'),
  path('product_show/<int:prod_id>/<int:img_id>',views.product_show,name='product_show'),
  path('user_category_show/<int:category_id>',views.user_category_show,name='user_category_show'),
  path('search_view/',views.search_view,name='search_view'),
  path('track_order/',views.track_order,name='track_order'),
  path('contact_page/',views.contact_page,name='contact_page'),
  path('contact_user/',views.contact_user,name='contact_user'),
  

   
]