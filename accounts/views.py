from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from products.models import Product  # Ensure you import the Product model
from django.views.generic import DetailView
from products.models import Product, Category, SubCategory  # Ensure ProductEnquiry is the correct model for inquiries
from enquiry.models import Enquiry
from django.conf import settings

class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.values('category').distinct()
        total_categories = Category.objects.all()

        product_list = []
        for item in products:
            top_products = Product.objects.filter(category=item['category']).order_by('-price')[:4]
            product_list.extend(top_products)

        context['products'] = product_list  # Keeping the variable name the same
        context['total_categories'] = total_categories 
        return context


import logging
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.db.models import Max
from .models import CustomUser
from .forms import CustomUserForm

logger = logging.getLogger(__name__)  # Setup logger

# Auto-generate username based on employee_id
def generate_username():
    try:
        max_id = CustomUser.objects.aggregate(Max('employee_id'))['employee_id__max'] or 0  # Get max ID safely
        next_id = max_id + 1  # Increment last ID
        username_prefix = getattr(settings, 'USERNAME_PREFIX', 'EMP')  # Fallback to 'EMP'
        return f"{username_prefix}{next_id:05d}"  # Format: EMP00001, EMP00002
    except Exception as e:
        logger.exception("Error generating username")
        return "EMP00001"  # Default fallback

# List Users (Read)
class UserListView(ListView):
    model = CustomUser
    template_name = 'admin_panel/user_crud.html'
    context_object_name = 'users'

from django.contrib import messages

class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'admin_panel/add_user.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            max_employee_id = CustomUser.objects.aggregate(Max('employee_id'))['employee_id__max'] or 0
            user.employee_id = max_employee_id + 1
            user.username = generate_username()
            user.save()
            messages.success(self.request, "User added successfully.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"An error occurred: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{form[field].label}: {error}")
        return super().form_invalid(form)



from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserForm

# Edit User (Update)
class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'admin_panel/user_crud.html'
    success_url = reverse_lazy('user_list')  # Redirect after update
    slug_field = "username"
    slug_url_kwarg = "username"

    def form_valid(self, form):
        messages.success(self.request, "User updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating user. Please check the form.")
        return super().form_invalid(form)


# Delete User
class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        user.delete()
        messages.success(request, f'User "{user.username}" has been deleted successfully.')
        return redirect('user_list')  # Redirect after deletion


from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import CustomUser  # Import your custom user model

class CustomLoginView(LoginView):
    template_name = "admin_panel/authentication-login.html"

    def form_valid(self, form):
        """Authenticate user against both User and CustomUser models."""
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        print(f"Attempting login for username: {username}")  # Debugging print

        # Try authenticating against the default User model
        user = authenticate(self.request, username=username, password=password)

        if user:
            print("User authenticated via Django default User model.")
            login(self.request, user)
            return redirect("dashboard")
        else:
            print("User not found in default User model.")

        # Try authenticating against CustomUser model
        try:
            custom_user = CustomUser.objects.get(username=username)
            if custom_user.check_password(password):
                print("User authenticated via CustomUser model.")
                login(self.request, custom_user)
                return redirect("dashboard")
            else:
                print("Password incorrect for CustomUser.")
        except CustomUser.DoesNotExist:
            print(f"CustomUser with username '{username}' does not exist.")

        # If both fail, show error message
        messages.error(self.request, "Invalid username or password.")
        print("Login failed: Invalid username or password.")
        return self.form_invalid(form)

@login_required
def dashboard_view(request):
    # Get counts
    total_products = Product.objects.all()
    total_categories = Category.objects.all()
    print("total_categoriestotal_categories", total_categories)
    total_subcategories = SubCategory.objects.all()
    total_enquiries = Enquiry.objects.count()
    total_cat_count = total_categories.count()
    total_subcat_count = total_subcategories.count()
    # unread_enquiries = Enquiry.objects.filter(is_read=False).count()
    # read_enquiries = Enquiry.objects.filter(is_read=True).count()

    context = {
        'total_products': total_products,
        'total_products_count' : total_products.count(),
        'total_categories': total_categories,
        'total_subcategories': total_subcategories,
        'total_enquiries': total_enquiries,
        'total_cat_count': total_cat_count,
        'total_subcat_count': total_subcat_count
        # 'unread_enquiries': unread_enquiries,
        # 'read_enquiries': read_enquiries,
    }
    return render(request, 'admin_panel/index.html', context)



from django.shortcuts import render
from products.models import Product, Category, SubCategory


def dashboard_search_list(request):
    query = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '').strip()
    subcategory_id = request.GET.get('subcategory', '').strip()

    total_products = Product.objects.all()
    total_categories = Category.objects.all()
    total_subcategories = SubCategory.objects.all()

    products = total_products  # Start with all products
    error_message = None

    if query or category_id or subcategory_id:
        if query:
            products = products.filter(name__icontains=query)  # Search by product name
        if category_id:
            products = products.filter(category_id=category_id)  # Filter by category
        if subcategory_id:
            products = products.filter(SubCategory_id=subcategory_id)  # Filter by subcategory
    else:
        error_message = "Please provide at least one search parameter."

    # ✅ Corrected way to print descriptions of all products
    for product in products:
        print("Product:", product.name, "| Description:", product.description)  # Debugging print

    return render(request, 'admin_panel/index.html', {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_subcategories': total_subcategories,
        'products': products,
        'query': query,
        'selected_category': category_id,
        'selected_subcategory': subcategory_id,
        'error_message': error_message,
    })


from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirects to the login page after logout



class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs["pk"])


def services_view(request):
    context={}
    total_categories = Category.objects.all()
    context['total_categories'] = total_categories 
    return render(request, 'services.html', context)


def about_view(request):
    context={}
    total_categories = Category.objects.all()
    context['total_categories'] = total_categories 
    return render(request, 'about.html', context)


import os
from django.http import FileResponse
from django.conf import settings

def download_database(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')  # Path to SQLite DB
    if os.path.exists(db_path):
        response = FileResponse(open(db_path, 'rb'), as_attachment=True, filename="database.sqlite3")
        return response
    else:
        return HttpResponse("Database file not found.", status=404)


