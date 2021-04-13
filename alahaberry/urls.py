"""alahaberry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from products.views import (ProductCreateView, ProductUpdateView, 
                            ProductDeleteView, AdminProductCreateView)
from users.views import UpdateAdView, DeleteAdView


urlpatterns = [
    # All-auth URLS
    #path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('signup/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password-reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    # User pages
    path('staff_dashboard/', user_views.staff_dashboard, name="staff-dashboard"),
    path('user_dashboard/', user_views.user_dashboard, name="user-dashboard"),
    path('user_dashboard/subscriptions/', user_views.subscriptions, name="subscriptions"),
    path('user_dashboard/add_product/', ProductCreateView.as_view(), name="create-product"),
    path('user_dashboard/update_product/<int:pk>/', ProductUpdateView.as_view(), name="update-product"),
    path('user_dashboard/delete_product/<int:pk>/', ProductDeleteView.as_view(), name="delete-product"),
    path('user_dashboard/individual_sales/', user_views.individual_sales, name="individual-sales"),
    path('staff_dashboard/add_product/', AdminProductCreateView.as_view(), name="admin-create-product"),
    path('staff_dashboard/manage_users/', user_views.manage_users, name="manage-users"),
    path('staff_dashboard/clerks/', user_views.manage_clerks, name="manage-clerks"),
    path('staff_dashboard/all_orders/', user_views.all_orders, name="all-orders"),
    path('staff_dashboard/all_orders/get_order_details/', user_views.get_order_details, name="order-details"),
    path('staff_dashboard/all_orders/make_delivery/', user_views.make_delivery, name="make-delivery"),
    
    path('staff_dashboard/deliver_order/', user_views.deliver_order, name="deliver-order"),
    path('staff_dashboard/all_subscriptions/', user_views.all_subscriptions, name="all-subscriptions"),
    path('staff_dashboard/item_sales/', user_views.item_sales, name="item-sales"),
    path('staff_dashboard/make_payment_to_seller/<int:s_id>/', user_views.make_payment_to_seller, name="make-payment-to-seller"),

    path('staff_dashboard/ad/<int:id>/', user_views.admin_view_ad, name="admin-ad-view"),
    path('staff_dashboard/edit_item/<int:id>/', user_views.admin_edit_item, name="admin-item-edit"),
    path('staff_dashboard/delete_item/<int:id>/', user_views.admin_delete_item, name="admin-item-delete"),
    path('staff_dashboard/activity_log/', user_views.activity_log, name="activity-log"),
    path('staff_dashboard/ajax/add_clerk/', user_views.admin_add_clerk, name="admin-add-clerk"),
    path('staff_dashboard/manage_ads/', user_views.manage_ads, name="manage-ads"),
    path('staff_dashboard/manage_ads/edit/<int:pk>/', UpdateAdView.as_view(), name="edit-ad"),
    path('staff_dashboard/manage_ads/delete/<int:pk>/', DeleteAdView.as_view(), name="delete-ad"),


    path('staff_dashboard/affiliations/', include('affiliations.urls')),
    path('staff_dashboard/subscription_packages/', include('subscription_packages.urls')),
    path('dashboard/profile/', include('users.urls')),
    path('products/', include('products.urls')),
    path('', include('alaha_market.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

