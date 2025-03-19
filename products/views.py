from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import CategoryForm, SubCategoryForm, ProductForm
from .models import SubCategory  # Import the model


def manage_items(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
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
            SubCategory.objects.create(name=name, description=description, category=category)
            return redirect("subcategory_list")

    return render(request, "admin_panel/add_SubCategory.html", {"categories": categories})

def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    categories = Category.objects.all()

    if request.method == "POST":
        subcategory.name = request.POST.get("name")
        subcategory.description = request.POST.get("description")
        category_id = request.POST.get("category")

        if category_id:
            subcategory.category = get_object_or_404(Category, id=category_id)

        subcategory.save()
        return redirect("subcategory_list")

    return render(request, "admin_panel/edit_SubCategory.html", {"subcategory": subcategory, "categories": categories})


def delete_subcategory(request, subcategory_id):
    print("Deleting SubCategory ID:", subcategory_id)
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)  # Renamed to `subcategory`
    subcategory.delete()
    return redirect('subcategory_list')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, SubCategory
from .forms import ProductForm

# --- Add/Edit Product View ---
def product_form_view(request, product_id=None):
    product = get_object_or_404(Product, id=product_id) if product_id else None
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    template = 'admin_panel/edit_product.html' if product else 'admin_panel/add_product.html'
    return render(request, template, {'form': form})

# --- Delete Product View ---
def delete_product(request, product_id):
    get_object_or_404(Product, id=product_id).delete()
    return redirect('product_list')



from django.shortcuts import render
from .models import Category, SubCategory, Product

def category_list(request):
    query = request.GET.get('search', '')  # Get the search query from the URL parameters
    categories = Category.objects.all()

    if query:
        categories = categories.filter(name__icontains=query)  # Filter categories by name

    return render(request, 'admin_panel/categories.html', {'categories': categories, 'query': query})

def subcategory_list(request):
    query = request.GET.get('search', '')  # Get search query
    subcategories = SubCategory.objects.all()

    if query:
        subcategories = subcategories.filter(name__icontains=query)  # Filter by name

    return render(request, 'admin_panel/subcategories.html', {'subcategories': subcategories, 'query': query})



def product_list(request):
    from django.shortcuts import render
    from .models import Product, Category, SubCategory
    query = request.GET.get('search', '')  # Get search query
    category_id = request.GET.get('category', '')  # Get selected category
    subcategory_id = request.GET.get('subcategory', '')  # Get selected subcategory

    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

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
from .models import Product, Category, SubCategory

# Product Grid View (Renamed)
def product_grid_view(request):
    query = request.GET.get('search', '')  # Get search query
    category_id = request.GET.get('category', '')  # Get selected category
    subcategory_id = request.GET.get('subcategory', '')  # Get selected subcategory

    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    if query:
        products = products.filter( Q(name__icontains=query) | Q(product_uid__icontains=query))  # Filter by product name
    if category_id:
        products = products.filter(category_id=category_id)  # Filter by category
    if subcategory_id:
        products = products.filter(SubCategory_id=subcategory_id)  # Filter by subcategory

    return render(request, 'product_detail_view.html', {
        'products': products,
        'categories': categories,
        'total_categories': categories,
        'subcategories': subcategories,
        'query': query,
        'selected_category': category_id,
        'selected_subcategory': subcategory_id,
    })


from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Fetch products from the same category (excluding current product)
    same_category_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]

    # Fetch products from the same subcategory (excluding current product)
    same_subcategory_products = Product.objects.filter(SubCategory=product.SubCategory).exclude(id=product.id)[:8] if product.SubCategory else []

    return render(request, 'product_detail.html', {
        'product': product,
        'same_category_products': same_category_products,
        'same_subcategory_products': same_subcategory_products
    })
