from django import forms
from .models import Product, Supplier, Category, Purchase, PurchaseDetail

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'category': forms.Select(attrs={'class': 'input-field'}),
            'supplier': forms.Select(attrs={'class': 'input-field'}),
            'price_buy': forms.NumberInput(attrs={'class': 'input-field'}),
            'price_sell': forms.NumberInput(attrs={'class': 'input-field'}),
            'stock': forms.NumberInput(attrs={'class': 'input-field'}),
            'stock_min': forms.NumberInput(attrs={'class': 'input-field'}),
            'expiration_date': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'phone': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'address': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'date', 'note']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'input-field'}),
            'date': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            'note': forms.Textarea(attrs={'class': 'input-field', 'rows': 2}),
        }

class PurchaseDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetail
        fields = ['product', 'quantity', 'price_unit']
        widgets = {
            'product': forms.Select(attrs={'class': 'input-field'}),
            'quantity': forms.NumberInput(attrs={'class': 'input-field'}),
            'price_unit': forms.NumberInput(attrs={'class': 'input-field'}),
        }

