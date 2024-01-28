from django import forms

class SignInForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)