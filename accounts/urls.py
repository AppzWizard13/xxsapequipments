from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView, CustomLoginView, DashboardView, DashboardSearchView,
    LogoutView, ServicesView, AboutView, DownloadDatabaseView,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
    ReviewListView, ReviewCreateView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView,
    BannerListView, BannerCreateView, BannerDetailView, BannerUpdateView, BannerDeleteView,
    DownloadAllMediaView
)

urlpatterns = [
    # Landing page
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Dashboard search
    path('dashboard/search/', DashboardSearchView.as_view(), name='dashboard_search_list'),

    # Static pages
    path('services/', ServicesView.as_view(), name='services'),
    path('about/', AboutView.as_view(), name='about'),
    path('download-db/', DownloadDatabaseView.as_view(), name='download_database'),

    # User management
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/edit/<str:username>/', UserUpdateView.as_view(), name='user_edit'),
    path('users/delete/<str:username>/', UserDeleteView.as_view(), name='user_delete'),

    # Review management
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/add/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('reviews/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),

    # Banner management
    path('banners/', BannerListView.as_view(), name='banner_list'),
    path('banners/create/', BannerCreateView.as_view(), name='banner_create'),
    path('banners/<int:pk>/', BannerDetailView.as_view(), name='banner_detail'),
    path('banners/<int:pk>/edit/', BannerUpdateView.as_view(), name='banner_edit'),
    path('banners/<int:pk>/delete/', BannerDeleteView.as_view(), name='banner_delete'),

    # Media download
    path('download-all-media/', DownloadAllMediaView.as_view(), name='download_all_media'),
]