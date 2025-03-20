from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

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
    product_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique identifier
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    # Main image
    images = models.ImageField(upload_to='product_images/')
    
    # Additional optional images
    image_1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='product_images/', blank=True, null=True)

    catalogues = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(subcategory, on_delete=models.CASCADE, related_name='products')

    price = models.DecimalField(max_digits=10, decimal_places=2)  # Added price field

    specifications = models.TextField()
    description = models.TextField()
    additional_information = models.TextField()

    def __str__(self):
        return self.name
