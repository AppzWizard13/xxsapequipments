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

        product_list = []
        for item in products:
            top_products = Product.objects.filter(category=item['category']).order_by('-price')[:4]
            product_list.extend(top_products)

        context['products'] = product_list  # Keeping the variable name the same
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

# Add User (Create)
class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'admin_panel/user_crud.html'
    success_url = reverse_lazy('user_list')  # Redirect after successful creation

    def form_valid(self, form):
        try:
            user = form.save(commit=False)

            # Get next employee ID in one query
            max_employee_id = CustomUser.objects.aggregate(Max('employee_id'))['employee_id__max'] or 0
            user.employee_id = max_employee_id + 1  # Assign next employee ID

            user.username = generate_username()  # Assign generated username
            user.save()
            
            return super().form_valid(form)
        except Exception as e:
            logger.exception("Error adding user")
            return self.form_invalid(form)


# Edit User (Update)
class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'admin_panel/user_crud.html'
    success_url = reverse_lazy('user_list')  # Redirect after update
    slug_field = "username"
    slug_url_kwarg = "username"


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser

class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        user.delete()
        return redirect('user_list')  # Redirect after deletion

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = "admin_panel/authentication-login.html"

    def form_valid(self, form):
        """Ensure user authentication before redirecting."""
        response = super().form_valid(form)  # Calls Django's built-in login process
        return redirect('dashboard')  # Redirects to dashboard after successful login

@login_required
def dashboard_view(request):
    # Get counts
    total_products = Product.objects.all()
    total_categories = Category.objects.all()
    total_subcategories = SubCategory.objects.all()
    # total_enquiries = Enquiry.objects.count()
    # unread_enquiries = Enquiry.objects.filter(is_read=False).count()
    # read_enquiries = Enquiry.objects.filter(is_read=True).count()

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_subcategories': total_subcategories,
        # 'total_enquiries': total_enquiries,
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
    return render(request, 'services.html')


def about_view(request):
    return render(request, 'about.html')


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


