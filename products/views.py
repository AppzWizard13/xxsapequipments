from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import CategoryForm, subcategoryForm, ProductForm
from .models import subcategory  # Import the model


def manage_items(request):
    categories = Category.objects.all()
    subcategories = subcategory.objects.all()
    products = Product.objects.all()
    
    return render(request, 'admin_panel/manage_items.html', {
        'categories': categories,
        'subcategories': subcategories,
        'products': products
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Import messages
from .forms import CategoryForm
from .models import Category

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)  # Include request.FILES for image uploads
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")  # Success message
            return redirect('category_list')
        else:
            messages.error(request, "There was an error adding the category. Please check the form.")  # Error message
    else:
        form = CategoryForm()
    
    return render(request, 'admin_panel/add_category.html', {'form': form})


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    print(f"Editing Category ID: {category.id}")  # Debugging

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")  # Success message
            return redirect('category_list')
        else:
            messages.error(request, "Error updating category. Please check the form.")  # Error message
    else:
        form = CategoryForm(instance=category)

    return render(request, 'admin_panel/edit_category.html', {'form': form, 'category': category})




def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')


def add_subcategory(request):
    categories = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        category_id = request.POST.get("category")

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            subcategory.objects.create(name=name, description=description, category=category)
            return redirect("subcategory_list")

    return render(request, "admin_panel/add_subcategory.html", {"categories": categories})

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import subcategory, Category

def edit_subcategory(request, subcategory_id):
    subcategory_instance = get_object_or_404(subcategory, id=subcategory_id)
    categories = Category.objects.all()

    if request.method == "POST":
        try:
            subcategory_instance.name = request.POST.get("name")
            subcategory_instance.description = request.POST.get("description")
            category_id = request.POST.get("category")

            if category_id:
                subcategory_instance.category = get_object_or_404(Category, id=category_id)

            subcategory_instance.save()
            messages.success(request, "Subcategory updated successfully!")
            return redirect("subcategory_list")
        except Exception as e:
            messages.error(request, f"Error updating subcategory: {str(e)}")
            return render(request, "admin_panel/edit_subcategory.html", {
                "subcategory": subcategory_instance,
                "categories": categories
            })

    return render(request, "admin_panel/edit_subcategory.html", {
        "subcategory": subcategory_instance,
        "categories": categories
    })

def delete_subcategory(request, subcategory_id):
    try:
        subcategory_instance = get_object_or_404(subcategory, id=subcategory_id)
        subcategory_instance.delete()
        messages.success(request, "Subcategory deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error deleting subcategory: {str(e)}")
    
    return redirect('subcategory_list')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category, subcategory
from .forms import ProductForm

def product_form_view(request, product_id=None):
    product = get_object_or_404(Product, id=product_id) if product_id else None
    action = "updated" if product else "added"
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Product successfully {action}!")
                return redirect('product_list')
            except Exception as e:
                messages.error(request, f"Error saving product: {str(e)}")
        else:
            # Form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProductForm(instance=product)

    template = 'admin_panel/edit_product.html' if product else 'admin_panel/add_product.html'
    return render(request, template, {
        'form': form,
        'product': product  # Pass product to template if needed
    })
# --- Delete Product View ---
def delete_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        product_name = product.name  # Get name before deletion
        product.delete()
        messages.success(request, f"Product '{product_name}' was successfully deleted!")
    except Exception as e:
        messages.error(request, f"Error deleting product: {str(e)}")
    
    return redirect('product_list')


from django.shortcuts import render
from .models import Category, subcategory, Product

def category_list(request):
    query = request.GET.get('search', '')  # Get the search query from the URL parameters
    categories = Category.objects.all()

    if query:
        categories = categories.filter(name__icontains=query)  # Filter categories by name

    return render(request, 'admin_panel/categories.html', {'categories': categories, 'query': query})

def subcategory_list(request):
    query = request.GET.get('search', '')  # Get search query
    subcategories = subcategory.objects.all()

    if query:
        subcategories = subcategories.filter(name__icontains=query)  # Filter by name

    return render(request, 'admin_panel/subcategories.html', {'subcategories': subcategories, 'query': query})



def product_list(request):
    from django.shortcuts import render
    from .models import Product, Category, subcategory
    query = request.GET.get('search', '')  # Get search query
    category_id = request.GET.get('category', '')  # Get selected category
    subcategory_id = request.GET.get('subcategory', '')  # Get selected subcategory

    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = subcategory.objects.all()

    if query:
        products = products.filter(name__icontains=query)  # Filter by product name
    if category_id:
        products = products.filter(category_id=category_id)  # ✅ Use `category_id`
    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)  # ✅ Use `subcategory_id` (case-sensitive)

    return render(request, 'admin_panel/products.html', {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
        'query': query,
        'selected_category': category_id,
        'selected_subcategory': subcategory_id,
    })



from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, subcategory

def product_grid_view(request, category_id=None):
    query = request.GET.get('search', '')  
    category_id = category_id or request.GET.get('category', '')  
    subcategory_id = request.GET.get('subcategory', '')  

    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = subcategory.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(product_uid__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)  
    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)

    return render(request, 'product_detail_view.html', {
        'products': products,
        'categories': categories,
        'total_categories': categories,
        'subcategories': subcategories,
        'query': query,
        'selected_category': str(category_id),  # Convert to string for template comparison
        'selected_subcategory': str(subcategory_id),  # Convert to string for template comparison
    })

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    print("categoriescategoriescategories", categories)

    # Fetch products from the same category (excluding current product)
    same_category_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]

    # Fetch products from the same subcategory (excluding current product)
    same_subcategory_products = Product.objects.filter(subcategory=product.subcategory).exclude(id=product.id)[:8] if product.subcategory else []

    return render(request, 'product_detail.html', {
        'product': product,
        'total_categories': categories,
        'same_category_products': same_category_products,
        'same_subcategory_products': same_subcategory_products
    })
