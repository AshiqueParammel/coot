from django.urls import path
from . import views

urlpatterns=[
        path('wish_list',views.wish_list,name='wish_list'),
        path('add_wish_list',views.add_wish_list,name='add_wish_list'),
        path('remove_wish_list/<int:wish_id>',views.remove_wish_list,name='remove_wish_list'),
      
]

