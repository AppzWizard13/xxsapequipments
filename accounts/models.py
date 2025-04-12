from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.timezone import now  # Fix the NameError issue
from .utils import compress_image  # Make sure to import this
from io import BytesIO

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field must be set")

        extra_fields.pop("username", None)  # Remove username if provided
        extra_fields.setdefault("is_active", True)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, blank=True, null=True)  
    phone_number = models.CharField(max_length=15, unique=True)
    employee_id = models.BigAutoField(primary_key=True)  
    join_date = models.DateField(auto_now_add=True)

    STAFF_ROLES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    ]
    staff_role = models.CharField(max_length=100, choices=STAFF_ROLES)

    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"EMP{str(self.employee_id).zfill(5)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"



class Review(models.Model):
    customer_name = models.CharField(max_length=255)
    review_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 rating
    review_content = models.TextField()
    review_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.customer_name} - {self.review_rating} Stars"


class Banner(models.Model):
    name = models.CharField(max_length=255)
    series = models.IntegerField()  # Changed to IntegerField
    image = models.ImageField(upload_to='banners/')
    image_1 = models.ImageField(upload_to='banners/')
    image_2 = models.ImageField(upload_to='banners/')
    image_3 = models.ImageField(upload_to='banners/')
    image_4 = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if image exists and compress it
        if self.image and hasattr(self.image, 'file'):
            self.image = compress_image(self.image)

        super().save(*args, **kwargs)