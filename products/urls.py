from django.urls import path
from .views import (ProductListView,CategoryDetailView,CategoryCreateView,
					CategoryUpdateView,CategoryDeleteView)
from . import views

urlpatterns = [
    #path('', ProductListView.as_view(), name="all-products"),
    #path('product/<int:pk>/', ProductDetailView.as_view(), name="product-detail"),
    path('product/add_product_image/<int:id>/', views.add_product_images, name="admin-add-product-image"),
    path('product/all_product_images/<int:id>/', views.all_product_images, name="all-product-images"),
	path('product/add_damage/<int:id>/', views.add_product_damage, name="add-product-damage"),
	path('product/add_item_color/<int:id>/', views.add_item_color, name="add-item-color"),
	path('product/edit_damage/<int:id>/', views.edit_damage, name="edit-damage"),
	path('product/edit_item_color/<int:id>/', views.edit_item_color, name="edit-item-color"),
	path('product/delete_damage/<int:id>/', views.delete_damage, name="delete-damage"),
	path('product/delete_item_color/<int:id>/', views.delete_item_color, name="delete-item-color"),
	path('categories/category/<int:pk>/', CategoryDetailView.as_view(), name="category-detail"),
	path('categories/add_category/', CategoryCreateView.as_view(), name="add-category"),
	path('categories/update_category/<int:pk>/', CategoryUpdateView.as_view(), name="update-category"),
	path('categories/delete_category/<int:pk>/', CategoryDeleteView.as_view(), name="delete-category"),
]



