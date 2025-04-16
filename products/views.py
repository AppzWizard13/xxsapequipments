from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from .models import Category, subcategory, Product
from .forms import CategoryForm, subcategoryForm, ProductForm

class ManageItemsView(LoginRequiredMixin, ListView):
    template_name = 'admin_panel/manage_items.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = subcategory.objects.all()
        context['products'] = Product.objects.all()
        return context

    def get_queryset(self):
        return None  # We're using get_context_data for multiple querysets

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'admin_panel/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            return Category.objects.filter(name__icontains=query)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search', '')
        return context

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin_panel/add_category.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Category added successfully!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error adding the category. Please check the form.")
        return super().form_invalid(form)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin_panel/edit_category.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Category updated successfully!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error updating category. Please check the form.")
        return super().form_invalid(form)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Category deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

# Subcategory Views
class SubcategoryListView(LoginRequiredMixin, ListView):
    model = subcategory
    template_name = 'admin_panel/subcategories.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            return subcategory.objects.filter(name__icontains=query)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search', '')
        return context

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class SubcategoryCreateView(LoginRequiredMixin, CreateView):
    model = subcategory
    template_name = 'admin_panel/add_subcategory.html'
    fields = ['name', 'description', 'category']
    success_url = reverse_lazy('subcategory_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Subcategory added successfully!")
        return response

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class SubcategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = subcategory
    template_name = 'admin_panel/edit_subcategory.html'
    fields = ['name', 'description', 'category']
    success_url = reverse_lazy('subcategory_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Subcategory updated successfully!")
        return response

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class SubcategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = subcategory
    success_url = reverse_lazy('subcategory_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Subcategory deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

# Product Views
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'admin_panel/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search', '')
        category_id = self.request.GET.get('category', '')
        subcategory_id = self.request.GET.get('subcategory', '')

        if query:
            queryset = queryset.filter(name__icontains=query)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = subcategory.objects.all()
        context['query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_subcategory'] = self.request.GET.get('subcategory', '')
        return context

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin_panel/add_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Product added successfully!")
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin_panel/edit_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Product updated successfully!")
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product_name = product.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Product '{product_name}' was successfully deleted!")
        return response

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

# Frontend Views
class ProductGridView(ListView):
    model = Product
    template_name = 'product_detail_view.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search', '')
        category_id = self.kwargs.get('category_id') or self.request.GET.get('category', '')
        subcategory_id = self.request.GET.get('subcategory', '')

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(product_uid__icontains=query))
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['total_categories'] = Category.objects.all()
        context['subcategories'] = subcategory.objects.all()
        context['query'] = self.request.GET.get('search', '')
        context['selected_category'] = str(self.kwargs.get('category_id') or self.request.GET.get('category', ''))
        context['selected_subcategory'] = str(self.request.GET.get('subcategory', ''))
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        total_categories = Category.objects.all().prefetch_related('products')
        
        # Prepare category data with products for navigation
        categories_with_products = []
        for category in total_categories:
            products = category.products.filter(is_active=True)
            categories_with_products.append({
                'category': category,
                'products': products
            })
        
        context.update({
            'total_categories': total_categories,
            'categories_with_products': categories_with_products,
            'same_category_products': Product.objects.filter(
                category=product.category
            ).exclude(id=product.id)[:8],
            'same_subcategory_products': Product.objects.filter(
                subcategory=product.subcategory
            ).exclude(id=product.id)[:8] if product.subcategory else []
        })
        return context