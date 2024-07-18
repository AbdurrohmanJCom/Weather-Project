from django import forms

class CityForm(forms.Form):
    city = forms.CharField(label='City', max_length=100)
