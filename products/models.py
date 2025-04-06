from django.db import models
import re

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    shortcut_image = models.ImageField(upload_to='category_shortcut_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField()

    def __str__(self):
        return self.name


import uuid
from django.db import models

class Product(models.Model):
    product_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    # Images
    images = models.ImageField(upload_to='product_images/')
    image_1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    popup_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    

    catalogues = models.CharField(max_length=255, blank=True, null=True)
    supplier_location = models.TextField(
        blank=True, 
        null=True,
        help_text="Comma-separated iframe codes for multiple locations. Example: '<iframe...>,<iframe...>'"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(subcategory, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    specifications = models.TextField()
    description = models.TextField()
    additional_information = models.TextField()

    def __str__(self):
        return self.name
                
    def get_supplier_location(self):
        """Returns a proper list of dictionaries containing iframe codes and shop names"""
        if not self.supplier_location:
            return []
        
        # First, split the string into individual iframes
        iframes = re.split(r',\s*(?=<iframe)', self.supplier_location.strip())
        
        # Clean each iframe and extract shop name
        cleaned_iframes = []
        for iframe in iframes:
            iframe = iframe.strip()
            if iframe:
                # Ensure proper closing tag
                if not iframe.endswith('</iframe>'):
                    iframe = iframe + '</iframe>'

                # Extract shop name using !2s pattern
                match = re.search(r"!2s([^!]*)", iframe)  # Extract text after "!2s"
                shop_name = match.group(1).replace("%20", " ") if match else "Unknown Shop"

                cleaned_iframes.append({"iframe": iframe, "shop_name": shop_name})

        return cleaned_iframes