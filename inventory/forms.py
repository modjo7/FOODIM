from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})

        # DEV added
        self.fields['itemname'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['username'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['expdate'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[0-2][0-2][0-9][0-9]-[0-1][0-9]-[0-3][0-9]', 'title' : 'Date type YYYY-MM-DD only'})
        #self.fields['expdate2'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[0-9][0-9][0-1][0-9][0-3][0-9]', 'title' : 'Date type YYYY-MM-DD only'})
        self.fields['desc'].widget.attrs.update({'class': 'textinput form-control'})

        #self.fields['picture_stock'].widget.attrs.update({'class': 'textinput form-control'})

        # END

    class Meta:
        model = Stock
        fields = ['name', 'itemname', 'quantity', 'username', 'expdate', 'desc', 'photo']

        # DEV added (for ordering by timeleft)
        ordering  =  [ '-timeleft' ]
