from django.urls import path
from . import views
from .views import (
    UserListView, UserCreateView, UserEditView, UserDeleteView,
    DashboardView, LoginView, LogoutView,AdminProductSummaryView
)

app_name = 'custom_admin'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:user_id>/edit/', UserEditView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('applications/', AdminProductSummaryView.as_view(), name='applications'),
    path('user_application/<int:user_id>/', views.UserProductListView.as_view(), name='user_application'),

]