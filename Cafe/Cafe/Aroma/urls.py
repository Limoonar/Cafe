from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('otp_verify/', views.otp_verify_view, name='otp_verify'),
    path('adminpage/', views.adminpage_view, name='adminpage'),
    path('adminpage/add_products/', views.add_products_view, name='add_products'),
    path('adminpage/inventory_management/', views.inventory_management_view, name='inventory_management'),
    # Other URLs for your views
]