from django import forms
from .models import CustomUser
from .utils import generate_username  # Import generate_username function

class CustomUserForm(forms.ModelForm):
    STAFF_ROLE_CHOICES = [
        ('sales', 'Sales'),
        ('accounts', 'Accounts'),
        ('production', 'Production'),
        ('admin', 'Admin'),
        ('customer_support', 'Customer Support'),
    ]

    staff_role = forms.ChoiceField(
        choices=STAFF_ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'employee_id', 'staff_role',
            'address', 'city', 'state', 'pincode', 'date_of_birth', 'gender',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # 'join_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Ensure join_date retains existing value
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Male', 'Male'), 
                ('Female', 'Female'), 
                ('Other', 'Other')
            ]),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Auto-generate employee_id if not provided
        if not instance.employee_id:
            latest_user = CustomUser.objects.order_by('-employee_id').first()
            instance.employee_id = (latest_user.employee_id + 1) if latest_user and latest_user.employee_id else 1  

        # Auto-generate username if not provided
        if not instance.username:
            instance.username = generate_username()

        if commit:
            instance.save()
        return instance


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