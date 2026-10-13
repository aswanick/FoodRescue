from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('hotel-dashboard/', views.hotel_dashboard, name='hotel_dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('userhome/', views.userhome, name='userhome'),
    path('add-food/', views.add_food, name='add_food'), 
    path('my-orders/', views.my_orders, name='my_orders'),
    path('place-order/<int:food_id>/', views.place_order, name='place_order'),
    path('edit-food/<int:food_id>/', views.edit_food, name='edit_food'),
    path('delete-food/<int:food_id>/', views.delete_food, name='delete_food'),
    path('hotel-orders/',views.hotel_orders,name='hotel_orders'),
    path('available-food/',views.available_food,name='available_food'),
    path('hotel-food/',views.hotel_food,name='hotel_food'),
    path('update-order-status/<int:order_id>/',views.update_order_status,name='update_order_status'),
    path('delivery-dashboard/',views.delivery_dashboard,name='delivery_dashboard'),
    path('accept-delivery/<int:order_id>/',views.accept_delivery,name='accept_delivery'),
    path('mark-delivered/<int:order_id>/',views.mark_delivered,name='mark_delivered'),
    path('complete-order/<int:order_id>/',views.complete_order,name='complete_order'),



]