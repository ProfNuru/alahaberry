from django.urls import path
from . import views
from users.views import AlahaBerrySettingUpdateView, DiscountSettingUpdateView

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('initialize_page/', views.initialize_page, name="initialize-page"),
    path('item_damages/', views.item_damages, name="item-damages"),
    path('item_colors/', views.item_colors, name="item-colors"),
    path('submit_order/', views.submit_order, name="submit-order"),
    
    path('<int:pk>/<productname>/', views.view_product, name="view-product"),
    # path('all_products/', views.all_products, name='search-products'),
    # path('new_products/', views.new_products, name='new-products'),
    # path('used_products/', views.used_products, name='used-products'),
    # path('shops/<int:pk>/<shopname>/', views.shops, name='shops'),
    # path('all_shops/', views.all_shops, name='all-shops'),
    path('category/<int:pk>/', views.category_view, name='category-page'),
    path('subscribe/', views.subscribe_to_newsletter, name='subscribe'),
    path('general_settings/<int:pk>/', AlahaBerrySettingUpdateView.as_view(), name='general-settings'),
    path('site_data/', views.get_site_data, name='site-data'),
    path('discount_settings/<int:pk>/', DiscountSettingUpdateView.as_view(), name='discount-settings'),
    # path('privacy_policy/', views.privacy_policy, name="privacy-policy"),
    # path('terms/', views.terms_of_service, name="terms-of-service")
]

