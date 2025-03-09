from django.urls import path
from .views import (
    manage_items, delete_category, delete_subcategory, delete_product,
    add_category, edit_category,
    add_subcategory, edit_subcategory,
    product_form_view, category_list, subcategory_list, product_list , product_grid_view, product_detail_view# ✅ Replaces add_product & edit_product
)


urlpatterns = [
    path('manage-items/', manage_items, name='manage_items'),

    # Category URLs
    path('add-category/', add_category, name='add_category'),
    path('edit-category/<int:category_id>/', edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),

    # SubCategory URLs
    path('add-SubCategory/', add_subcategory, name='add_subcategory'),
    path('edit-SubCategory/<int:subcategory_id>/', edit_subcategory, name='edit_subcategory'),
    path('delete-SubCategory/<int:subcategory_id>/', delete_subcategory, name='delete_subcategory'),

    # Product URLs
    path('product/add/', product_form_view, name='add_product'),  # ✅ Handles adding a product
    path('product/edit/<int:product_id>/', product_form_view, name='edit_product'),  # ✅ Handles editing a product
    path('product/delete/<int:product_id>/', delete_product, name='delete_product'),  


    path('categories/', category_list, name='category_list'),
    path('subcategories/', subcategory_list, name='subcategory_list'),
    path('products/', product_list, name='product_list'),

    path('products-grid/', product_grid_view, name='product_grid_view'),  # Updated route
    path('products/<int:product_id>/', product_detail_view, name='product_detail'),
]
