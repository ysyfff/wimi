from django import forms

class AddFoodForm(forms.Form):
    name = forms.CharField(max_length=50)
    price = forms.FloatField()