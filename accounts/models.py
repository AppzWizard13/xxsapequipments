from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    employee_id = models.AutoField(primary_key=True)
    join_date = models.DateField(auto_now_add=True)
    staff_role = models.CharField(max_length=100)

    # Newly added fields
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)  # To enable/disable users

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"


from django.utils.timezone import now

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

    def __str__(self):
        return self.name