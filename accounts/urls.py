from . import views
from django.urls import path
from django.contrib import admin
from accounts.views import CustomLoginView, dashboard_view, logout_view
from django.contrib.auth import views as auth_views
from .views import *
from .views import review_list, review_create, review_edit, review_delete, review_detail


urlpatterns = [
    # landing page
    path('', views.HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),

    # path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('dashboard/search/', views.dashboard_search_list, name='dashboard_search_list'),


    path('services/', views.services_view, name='services'),
    path('about/', views.about_view, name='about'),
    path('download-db/', views.download_database, name='download_database'),

    path('users/', UserListView.as_view(), name='user_list'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/edit/<str:username>/', UserUpdateView.as_view(), name='user_edit'),
    path('users/delete/<str:username>/', UserDeleteView.as_view(), name='user_delete'),


    path('reviews/', review_list, name='review_list'),
    path('reviews/add/', review_create, name='review_create'),
    path('reviews/<int:pk>/', review_detail, name='review_detail'),
    path('reviews/<int:pk>/edit/', review_edit, name='review_edit'),
    path('reviews/<int:pk>/delete/', review_delete, name='review_delete'),











    
]