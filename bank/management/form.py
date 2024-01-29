from django import forms
from django.utils import timezone
import uuid
import random

class SignInForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)

class CreateAccForm(forms.Form):
    owner = forms.CharField(max_length=32)
    balance = forms.IntegerField()
    password = forms.CharField(max_length=8)
    acc_number = forms.CharField(max_length=32)
    date_open = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),initial=timezone.now())
    date_closed = forms.DateField(required=False)
    rate = forms.FloatField(required=False)
    acc_status = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['acc_number'].initial = str(uuid.uuid4())[:20]
        self.fields['acc_number'].initial = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        self.fields['acc_number'].widget.attrs['readonly'] = True

        self.fields['owner'].widget.attrs.update({'class': 'form-control'})
        self.fields['owner'].widget.attrs['readonly'] = True

        self.fields['balance'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['acc_number'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['acc_status'].widget.attrs.update({'class': 'form-check-input'})


    