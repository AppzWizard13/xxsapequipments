from django import forms
from .models import *
from .utils import compress_image  # or wherever your compress_image function is
from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'shortcut_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



class subcategoryForm(forms.ModelForm):
    class Meta:
        model = subcategory
        fields = ['name', 'category', 'description']

    def __init__(self, *args, **kwargs):
        super(subcategoryForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()

        if categories.exists():
            self.fields['category'].queryset = categories
        else:
            self.fields['category'].choices = [("", "No Category Found")]
            self.fields['category'].widget.attrs['disabled'] = 'disabled'  # Disable dropdown



from django import forms
from .models import Product
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from markdownx.widgets import MarkdownxWidget
from django.conf import settings
import os



class ProductForm(forms.ModelForm):
    image_1 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    image_2 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    image_3 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    popup_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}))
    ytlink_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}))
    catalogues = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))  # ✅ Optional PDF upload

    class Meta:
        model = Product
        fields = [
            'name', 'is_active', 'images', 'image_1', 'image_2', 'image_3', 'popup_image',
            'catalogues', 'supplier_location', 'youtube_url', 'category', 'price',
            'subcategory', 'specifications', 'description', 'additional_information',
            'sku', 'ytlink_image'
        ]
        widgets = {
            'specifications': MarkdownxWidget(attrs={'class': 'form-control'}),
            'description': MarkdownxWidget(attrs={'class': 'form-control'}),
            'additional_information': MarkdownxWidget(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'youtube_url': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_location': forms.TextInput(attrs={'class': 'form-control'}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_catalogues(self):
        catalogue = self.cleaned_data.get('catalogues', None)
        if catalogue:
            try:
                if catalogue.size > 300 * 1024:
                    raise ValidationError("Catalogue file size should not exceed 300KB.")
                if not catalogue.name.endswith('.pdf'):
                    raise ValidationError("Only PDF files are allowed for catalogues.")
            except FileNotFoundError:
                raise ValidationError("The uploaded catalogue file is missing. Please upload a new file.")
        else:
            # If editing and file might have been deleted on disk
            if self.instance and self.instance.catalogues:
                full_path = os.path.join(settings.MEDIA_ROOT, str(self.instance.catalogues))
                if not os.path.exists(full_path):
                    raise ValidationError("The existing catalogue file is missing. Please upload a new one.")
        return catalogue
