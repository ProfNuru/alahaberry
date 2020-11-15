from django.urls import path
from . import views
from .views import UpdatePackageView, DeletePackageView

urlpatterns = [
    path('', views.all_packages, name="all-packages"),
    path('view_package/<int:id>/', views.view_package, name="view-package"),
    path('edit_package/<int:pk>/', UpdatePackageView.as_view(), name="edit-package"),
    path('delete_package/<int:pk>/', DeletePackageView.as_view(), name="delete-package"),
]

