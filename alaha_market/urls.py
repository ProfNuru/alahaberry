from django.urls import path
from . import views
from users.views import AlahaBerrySettingUpdateView, DiscountSettingUpdateView

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('<int:pk>/<productname>/', views.view_product, name="view-product"),
    path('all_products/', views.all_products, name='search-products'),
    path('new_products/', views.new_products, name='new-products'),
    path('used_products/', views.used_products, name='used-products'),
    path('shops/<int:pk>/<shopname>/', views.shops, name='shops'),
    path('all_shops/', views.all_shops, name='all-shops'),
    path('category/<int:pk>/', views.category_view, name='category-page'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('general_settings/<int:pk>/', AlahaBerrySettingUpdateView.as_view(), name='general-settings'),
    path('discount_settings/<int:pk>/', DiscountSettingUpdateView.as_view(), name='discount-settings'),
    path('privacy_policy/', views.privacy_policy, name="privacy-policy"),
    path('terms/', views.terms_of_service, name="terms-of-service")    
]

