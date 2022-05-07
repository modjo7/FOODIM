from django import forms
from django.forms import formset_factory
from .models import (
    Item,
    PurchaseArticle, 
    PurchaseItem,
    PurchaseArticleDetails, 
    SaleArticle, 
    SaleItem,
    SaleArticleDetails
)
from inventory.models import Stock


# form used to select a item
class SelectItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(is_deleted=False)
        self.fields['item'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = PurchaseArticle
        fields = ['item']

# form used to render a single stock item form
class PurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = PurchaseItem
        fields = ['stock', 'quantity', 'perprice']

# formset used to render multiple 'PurchaseItemForm'
PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)

# form used to accept the other details for purchase article
class PurchaseDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '200', 'title': 'Title Required'})
        self.fields['contact'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '100', 'title': 'Contact Required'})
        self.fields['comment'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '300', 'title': 'Comment Required'})
        self.fields['address'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '300', 'title': 'Address Required'})

    class Meta:
        model = PurchaseArticleDetails
        fields = ['title', 'address', 'contact', 'comment']


# form used for item
class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['protein'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['fat'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['carbohydrate'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only'})
        self.fields['vitamin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only'})
        self.fields['desc'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '300', 'title' : 'Description Required'})

    class Meta:
        model = Item
        fields = ['name', 'protein', 'fat', 'carbohydrate', 'vitamin', 'desc']

# form used to get customer details
class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '200', 'title': 'Title Required'})
        self.fields['contact'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '100', 'title': 'Contact Required'})
        self.fields['comment'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '300', 'title': 'Comment Required'})

    class Meta:
        model = SaleArticle
        fields = ['title', 'contact', 'comment']

# form used to render a single stock item form
class SaleItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = SaleItem
        fields = ['stock', 'quantity', 'perprice']

# formset used to render multiple 'SaleItemForm'
SaleItemFormset = formset_factory(SaleItemForm, extra=1)

# form used to accept the other details for sales article
class SaleDetailsForm(forms.ModelForm):
    class Meta:
        model = SaleArticleDetails
        fields = ['address']
