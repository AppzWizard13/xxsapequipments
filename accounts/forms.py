from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.db.models import Max
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Max
from .models import CustomUser

class CustomUserForm(UserCreationForm):
    password1 = forms.CharField(
        required=False,  # Make password optional
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="Password"
    )
    password2 = forms.CharField(
        required=False,  # Make password optional
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'email', 'staff_role',
            'address', 'city', 'state', 'pincode', 'date_of_birth', 'gender',
            'password1', 'password2', 'is_active', 'is_staff',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pincode'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Male', 'Male'), 
                ('Female', 'Female'), 
                ('Other', 'Other')
            ]),
            'staff_role': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Admin', 'Admin'), 
                ('Manager', 'Manager'), 
                ('Employee', 'Employee')
            ]),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If updating an existing user, make password fields optional
        if self.instance and self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Auto-generate employee_id
        if not instance.employee_id:
            max_employee_id = CustomUser.objects.aggregate(Max('employee_id'))['employee_id__max'] or 0
            instance.employee_id = max_employee_id + 1  

        # Auto-generate username
        instance.username = f"EMP{str(instance.employee_id).zfill(5)}"

        # Set password only if provided
        if self.cleaned_data.get('password1'):
            instance.set_password(self.cleaned_data['password1'])

        if commit:
            instance.save()
        return instance



User = get_user_model()

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone number"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("username")

        # Ensure phone number exists
        if phone_number and not User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number not found.")

        return cleaned_data

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['customer_name', 'review_rating', 'review_content', 'review_date']
        widgets = {
            'review_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            print("self.instance.review_dateself.instance.review_date", self.instance.review_date)
            self.fields['review_date'].initial = self.instance.review_date


from django import forms
from .models import Banner

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['name', 'series', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'series': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BannerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'