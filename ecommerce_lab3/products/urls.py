from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Public URLs
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),

    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Admin - Category CRUD
    path('admin/categories/', views.category_list, name='category_list'),
    path('admin/categories/create/', views.category_create, name='category_create'),
    path('admin/categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('admin/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Admin - Product CRUD
    path('admin/products/', views.product_list_admin, name='product_list_admin'),
    path('admin/products/create/', views.product_create, name='product_create'),
    path('admin/products/<int:pk>/update/', views.product_update, name='product_update'),
    path('admin/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
