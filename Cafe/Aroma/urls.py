from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('otp_verify/', views.otp_verify_view, name='otp_verify'),
    # ADMIN
    path('adminpage/', views.adminpage_view, name='adminpage'),
    path('adminpage/add_products/', views.add_products_view, name='add_products'),
    path('adminpage/inventory_management/', views.inventory_management_view, name='inventory_management'),
    path('adminpage/inventory_update/', views.inventory_update_view , name = 'inventory_update'),
    # CUSTOMER
    path('customerpage/', views.customerpage_view, name='customerpage'),
    path('customerpage/purchase/', views.purchase_view, name='purchase'),
    #path('customerpage/purchase/success/', views.purchase_success_view, name='purchase_success'),
    # PRODUCTS
    path('products/', views.products_page_view, name='products'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    #path('update_pickup_type/', views.update_pickup_type, name='update_pickup_type'),
    path('finalize-purchase/', views.finalize_purchase, name='finalize_purchase'),
    path('thank-you/', views.render, {'template_name': 'thank_you.html'}, name='thank_you'),
    path('order_history/', views.order_history, name='order_history'),
    path('api/orders/', views.filter_orders, name='filter_orders'),
    path('api/best-selling-products/', views.best_selling_products_api, name='best_selling_products_api'),

    # Other URLs for your views
]