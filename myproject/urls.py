"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login_user')),
    path('user/login/', views.login_user, name='login_user'),   # Trang user
    path('user/register/', views.register_user, name='register_user'),   # Trang user
    path('user/home/', views.home_user, name='home_user'),   
    path('user/about/', views.about_user, name='about_user'), 
    path('user/product/', views.product_user, name='product_user'),   
    path('user/blog/', views.blog_user, name='blog_user'),  
    path('user/profile/', views.profile_user, name='profile_user'),  
    path('manager/homemproduct/', views.home_product_manager, name='home_product_manager'), # Trang admin
    path('user/cart/', views.cart_user, name='cart_user'),
    path('user/cart/delete/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('manager/mproducttype/', views.mproducttype_manager, name='mproducttype_manager'), # Trang admin
    path('manager/login/', views.login_manager, name='login_manager'), # Trang admin
    path('manager/check-product-type-code/', views.check_product_type_code, name='check_product_type_code'),# Trang admin
    path('manager/add-product-type/', views.add_product_type, name='add_product_type'),# Trang admin
    path('manager/delete-product-types/', views.delete_product_types, name='delete_product_types'),# Trang admin
    path('manager/update-product-types/', views.update_product_types, name='update_product_types'),# Trang admin
    path('manager/mproduct/', views.mproduct_manager, name='mproduct_manager'),
    path('manager/add-product/', views.add_product, name='add_product'),
    path('api/product/<int:product_id>/', views.get_product_details, name='get_product_details'),
    path('manager/delete-products/', views.delete_selected_products, name='delete_selected_products'),
    path('manager/edit-product/', views.edit_product, name='edit_product'),
    path('user/checkout/', views.checkout_view, name='checkout'),
    path('user/payment/', views.payment_user, name='payment_user'),
    path('user/checkout/details/', views.checkout_details_view, name='checkout_details'),
    path('user/payment_user/', views.payment_user, name='payment_user'),
    path('api/create-order/', views.create_order, name='create_order'),
    path('manager/home/', views.home_manager, name='home_manager'), # Trang admin
    path('manager/homemorder/', views.home_order_manager, name='home_order_manager'), # Trang admin
    path('manager/morderwait/', views.order_wait_confirm_management, name='order_wait_confirm_management'),  # ✅ THÊM DÒNG NÀY
    path('manager/orderwaitdetail/', views.order_wait_confirm_detail, name='order_wait_confirm_detail'), # Trang admin
    path('manager/createorder/', views.create_order_manage, name='create_order_manage'), # Trang admin
    path('manager/orderwaitdetail/<int:order_id>/', views.order_wait_confirm_detail, name='order_wait_confirm_detail'),  # ✅ Trang chi tiết đơn hàng
    path('manager/order-header/create/', views.create_order_header, name='create_order_header'),
    path('manager/muser/', views.user_manage, name='user_manage'), # Trang admin
    path('manager/muserdetail/<int:user_id>/', views.user_manage_detail, name='user_manage_detail'),
    path('manager/revenue/', views.manage_revenue, name='manage_revenue'), # Trang admin
    path('manager/allorder/', views.all_order, name='all_order'), # Trang admin
    path('manager/orderdetail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('manager/get-user-by-phone/',views.get_user_by_phone,name='get_user_by_phone'),
    path("save-order/",views.save_order, name="save_order" ),
    path("favorite-product/", views.favorite_product, name="favorite_product"),
    path('user/favorite/', views.favorite_user, name='favorite_user'),  
    path("save-location/", views.save_location, name="save_location"),
    path('user/update-profile/', views.update_profile_user, name='update_profile_user'),
    path('manager/revenue/api/', views.revenue_api, name='revenue_api'),
    path("manager/favorite-product-api/", views.favorite_product_api, name="favorite_product_api"),
    path("manager/best-selling-product-api/", views.best_selling_product_api, name="best_selling_product_api"),
    path('manager/export-products/', views.export_products_excel,name='export_products_excel'),
    path('manager/import-products/',views.import_products_excel,name='import_products_excel'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)