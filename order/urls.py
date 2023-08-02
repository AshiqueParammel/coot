from django.urls import path
from . import views

urlpatterns=[
    
    path('order_list/',views.order_list,name='order_list'),
    path('order_view/<int:view_id>',views.order_view,name='order_view'),
    path('change_status/',views.change_status,name='change_status'),
    path('change_status_order/',views.change_status_order,name='change_status_order'),

]