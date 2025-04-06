from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse, FileResponse
from django.conf import settings
from django.db.models import Max
import os
import zipfile
from io import BytesIO
import logging
from .forms import CustomUserForm, UserLoginForm
from products.models import Product, Category, subcategory
from enquiry.models import Enquiry
from .models import CustomUser, Banner, Review
from .forms import CustomUserForm, ReviewForm, BannerForm
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
import os
import zipfile
from io import BytesIO
from .models import Review, Banner
from .forms import ReviewForm, BannerForm

logger = logging.getLogger(__name__)

CustomUser = get_user_model()


# Home Page View
class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_categories = Category.objects.all().prefetch_related('products')
        products = Product.objects.values('category').distinct()
        reviews = Review.objects.all()
        banners = Banner.objects.all().order_by('series')

        product_list = []
        for item in products:
            top_products = Product.objects.filter(category=item['category']).order_by('-price')[:4]
            product_list.extend(top_products)

        category_data = {}
        for category in total_categories:
            products = category.products.filter(is_active=True).values('id', 'name', 'price')[:4]
            category_data[category.id] = list(products)

        context.update({
            'is_mobile': self.request.user_agent.is_mobile,
            'reviews': reviews,
            'total_categories': total_categories,
            'products': product_list,
            'category_data': category_data,
            'banners': banners,
        })
        return context


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_categories'] = Category.objects.all()
        return context


# API View
class FetchProductsView(View):
    def get(self, request, *args, **kwargs):
        category_id = self.kwargs['category_id']
        products = Product.objects.filter(
            category_id=category_id, 
            is_active=True
        ).values('id', 'name', 'price')
        return JsonResponse(list(products), safe=False)




# Logout View
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

# Dashboard Views
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_products': Product.objects.all(),
            'total_products_count': Product.objects.count(),
            'total_categories': Category.objects.all(),
            'total_subcategories': subcategory.objects.all(),
            'total_enquiries': Enquiry.objects.count(),
            'total_cat_count': Category.objects.count(),
            'total_subcat_count': subcategory.objects.count(),
        })
        return context

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class DashboardSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search', '').strip()
        category_id = self.request.GET.get('category', '').strip()
        subcategory_id = self.request.GET.get('subcategory', '').strip()

        products = Product.objects.all()
        error_message = None

        if query or category_id or subcategory_id:
            if query:
                products = products.filter(name__icontains=query)
            if category_id:
                products = products.filter(category_id=category_id)
            if subcategory_id:
                products = products.filter(subcategory_id=subcategory_id)
        else:
            error_message = "Please provide at least one search parameter."

        context.update({
            'total_products': Product.objects.all(),
            'total_categories': Category.objects.all(),
            'total_subcategories': subcategory.objects.all(),
            'products': products,
            'query': query,
            'selected_category': category_id,
            'selected_subcategory': subcategory_id,
            'error_message': error_message,
        })
        return context

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

# Static Pages
class ServicesView(TemplateView):
    template_name = 'services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_categories'] = Category.objects.all()
        return context

# User Management Views
class UserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'admin_panel/add_user.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        try:
            user = form.save(commit=False)

            # Use password1 instead of password
            if 'password1' in form.cleaned_data:
                user.set_password(form.cleaned_data['password1'])  # Correct field

            # Generate employee_id
            max_employee_id = CustomUser.objects.aggregate(Max('employee_id'))['employee_id__max'] or 0
            user.employee_id = max_employee_id + 1

            # Generate username
            user.username = self.generate_username(user.employee_id)

            user.save()
            messages.success(self.request, "User added successfully.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"An error occurred: {str(e)}")
            return self.form_invalid(form)

    def generate_username(self, employee_id):
        """Generate unique username like EMP00001."""
        return f"EMP{str(employee_id).zfill(5)}"

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserForm
    template_name = 'admin_panel/user_crud.html'
    success_url = reverse_lazy('user_list')
    slug_field = "username"
    slug_url_kwarg = "username"

    def form_valid(self, form):
        user = form.save(commit=False)

        # Get password only if provided
        password = form.cleaned_data.get("password1")  # Use 'password1' instead of 'password'
        if password:
            user.set_password(password)  # Only set password if it's provided

        user.save()
        messages.success(self.request, "User updated successfully.")
        return super().form_valid(form)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class CustomLoginView(LoginView):
    template_name = "admin_panel/authentication-login.html"
    form_class = UserLoginForm  # Use custom login form

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, "Login successful!")  # Add success message
        return redirect("dashboard")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid phone number or password.")
        return super().form_invalid(form)

class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'admin_panel/user_crud.html'
    context_object_name = 'users'

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    slug_field = "username"
    slug_url_kwarg = "username"
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'User has been deleted successfully.')
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


# Review Management Views
class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'admin_panel/review_list.html'
    context_object_name = 'reviews'

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'admin_panel/review_form.html'
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):
        messages.success(self.request, "Review added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error adding the review. Please check the form.")
        return super().form_invalid(form)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'admin_panel/review_detail.html'
    context_object_name = 'review'

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'admin_panel/review_form.html'
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):
        messages.success(self.request, "Review updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating review. Please check the form.")
        return super().form_invalid(form)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('review_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Review deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

# Banner Management Views
class BannerListView(LoginRequiredMixin, ListView):
    model = Banner
    template_name = 'admin_panel/banner_list.html'
    context_object_name = 'banners'

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class BannerCreateView(LoginRequiredMixin, CreateView):
    model = Banner
    form_class = BannerForm
    template_name = 'admin_panel/banner_form.html'
    success_url = reverse_lazy('banner_list')

    def form_valid(self, form):
        messages.success(self.request, "Banner added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error adding the banner. Please check the form.")
        return super().form_invalid(form)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class BannerDetailView(LoginRequiredMixin, DetailView):
    model = Banner
    template_name = 'admin_panel/banner_detail.html'
    context_object_name = 'banner'

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class BannerUpdateView(LoginRequiredMixin, UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = 'admin_panel/banner_form.html'
    success_url = reverse_lazy('banner_list')

    def form_valid(self, form):
        messages.success(self.request, "Banner updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating banner. Please check the form.")
        return super().form_invalid(form)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class BannerDeleteView(LoginRequiredMixin, DeleteView):
    model = Banner
    success_url = reverse_lazy('banner_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Banner deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

# Utility Views
class DownloadDatabaseView(LoginRequiredMixin, View):
    def get(self, request):
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        if os.path.exists(db_path):
            response = FileResponse(open(db_path, 'rb'), as_attachment=True, filename="database.sqlite3")
            return response
        return HttpResponse("Database file not found.", status=404)

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class DownloadAllMediaView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            memory_buffer = BytesIO()
            with zipfile.ZipFile(memory_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                media_root = str(settings.MEDIA_ROOT)
                for root, _, files in os.walk(media_root):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if file_path.startswith(media_root):
                            arcname = os.path.relpath(file_path, media_root)
                            zipf.write(file_path, arcname)

            memory_buffer.seek(0)
            response = HttpResponse(memory_buffer.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="all_media_files.zip"'
            memory_buffer.close()
            return response
            
        except Exception as e:
            if 'memory_buffer' in locals():
                memory_buffer.close()
            return HttpResponse(f"Error creating archive: {str(e)}", status=500, content_type='text/plain')

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())