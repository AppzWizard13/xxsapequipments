from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category', 'description']

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()

        if categories.exists():
            self.fields['category'].queryset = categories
        else:
            self.fields['category'].choices = [("", "No Category Found")]
            self.fields['category'].widget.attrs['disabled'] = 'disabled'  # Disable dropdown



from django import forms
from .models import Product
from django.utils.safestring import mark_safe
from markdownx.widgets import MarkdownxWidget

class ProductForm(forms.ModelForm):
    image_1 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    image_2 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    image_3 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = [
            'name', 'is_active', 'images', 'image_1', 'image_2', 'image_3', 'catalogues',
            'category', 'price', 'SubCategory', 'specifications', 'description', 'additional_information'
        ]
        widgets = {
            'specifications': MarkdownxWidget(attrs={'class': 'form-control'}),
            'description': MarkdownxWidget(attrs={'class': 'form-control'}),
            'additional_information': MarkdownxWidget(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'SubCategory': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'catalogues': forms.TextInput(attrs={'class': 'form-control'}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
