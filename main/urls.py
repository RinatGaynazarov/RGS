from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView, LogoutView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add/', ProductCreateView.as_view(), name='product-add'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product-edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
]

