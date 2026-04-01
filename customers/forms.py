from django import forms

from giftkeepers.models import  Customertbl,CustomerOrders

class CustomersForm(forms.ModelForm):
    class Meta: 
        model = Customertbl
        fields ='__all__'

        widgets={
            'name' : forms.TextInput(attrs={'required': True,'onkeypress': 'return isNumberKey(event);'}),
            'contactNo': forms.TextInput(attrs={'required': True, 'maxlength':"10", 'onkeypress': 'return restrictAlphabets(event);'}),
            'password': forms.TextInput(attrs={'type': 'password'}),
        }   

class OrderForm(forms.ModelForm):
    class Meta:
        model =  CustomerOrders
        fields='__all__'
        exclude = ['invno','qty','price','totalprice','status','totalcost','currentdate']
            