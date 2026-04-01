from django import forms
from .models import City, Area, Employee,Admintbl

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admintbl
        fields ='__all__'

        widgets={
            'username': forms.TextInput(attrs={'required': True,'class':'form-control'}),
            'password': forms.TextInput(attrs={'required': True,'class':'form-control'})
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'
        
        widgets={
            'cityName': forms.TextInput(attrs={'required': True,'onkeypress': 'return isNumberKey(event);'})
        }

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'

        widgets={
               'areaName' : forms.TextInput(attrs={'required': True,'onkeypress': 'return isNumberKey(event);'})
        }

class EmployeeForm(forms.ModelForm):
    class Meta: 
        model = Employee
        fields = '__all__'

        widgets={
            'name' : forms.TextInput(attrs={'required': True,'onkeypress': 'return isNumberKey(event);'}),
            'address' : forms.TextInput(attrs={'required': True,'onkeypress': 'return isNumberKey(event);'}),
            'contactNo': forms.TextInput(attrs={'required': True, 'maxlength':"10", 'onkeypress': 'return restrictAlphabets(event);'}),
        }        