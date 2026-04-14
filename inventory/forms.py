from django import forms
from .models import Product, Sale, StockReceipt


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'supplier',
            'gender',
            'size',
            'color',
            'article',
            'price',
            'quantity',
            'minimum_quantity',
        ]
        labels = {
            'name': 'Наименование',
            'category': 'Категория',
            'supplier': 'Поставщик',
            'gender': 'Пол',
            'size': 'Размер',
            'color': 'Цвет',
            'article': 'Артикул',
            'price': 'Цена',
            'quantity': 'Количество',
            'minimum_quantity': 'Минимальный остаток',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите название товара'}),
            'size': forms.TextInput(attrs={'placeholder': 'Например: S, M, L'}),
            'color': forms.TextInput(attrs={'placeholder': 'Например: Белый'}),
            'article': forms.TextInput(attrs={'placeholder': 'Введите артикул'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'min': '0'}),
            'minimum_quantity': forms.NumberInput(attrs={'min': '0'}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity', 'comment']
        labels = {
            'product': 'Товар',
            'quantity': 'Количество',
            'comment': 'Комментарий',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': '1'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


class StockReceiptForm(forms.ModelForm):
    class Meta:
        model = StockReceipt
        fields = ['product', 'quantity', 'supplier', 'comment']
        labels = {
            'product': 'Товар',
            'quantity': 'Количество',
            'supplier': 'Поставщик',
            'comment': 'Комментарий',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': '1'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
