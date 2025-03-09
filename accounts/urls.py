from . import views
from django.urls import path
from django.contrib import admin
from accounts.views import CustomLoginView, dashboard_view, logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # landing page
    path('', views.HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),

    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('dashboard/search/', views.dashboard_search_list, name='dashboard_search_list'),


    path('services/', views.services_view, name='services'),
    path('about/', views.about_view, name='about'),








    
]