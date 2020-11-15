from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_affiliates, name="all-affiliates"),
    path('sales_person/', views.sales_person, name="sales-person"),
    path('add_affiliate/', views.admin_add_affiliate, name="add-affiliate"),
    path('edit_coupon_code/<int:id>/', views.edit_coupon_code, name="edit-coupon-code"),
    path('commissions/<int:id>/', views.commissions, name="commissions"),
    path('pay_commission/<int:cid>/<int:aid>/', views.pay_commission, name="pay-commission"),
    path('pay_all_commissions/<int:aid>/', views.pay_all_commissions, name="pay-all-commissions"),
    path('be_an_affiliate/<int:id>/', views.be_an_affiliate, name="be-an-affiliate"),
]

