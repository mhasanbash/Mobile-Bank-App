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

class MakeTransactionForm(forms.Form):
    src_account_number = forms.CharField(max_length=32)
    dst_account_number = forms.CharField(max_length=32)
    amount = forms.IntegerField()
    password = forms.CharField(max_length=32)
    name = forms.CharField(max_length=32)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['src_account_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['src_account_number'].widget.attrs.update({'id': 'src_account_number'})

        self.fields['dst_account_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['dst_account_number'].widget.attrs.update({'id': 'dst_account_number'})
        
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'id': 'name'})
        self.fields['name'].widget.attrs['readonly'] = True

        self.fields['password'].widget.attrs.update({'id': 'password'})
        # self.fields['password'].widget.attrs.update({'style': 'display: none;'})
        
        
        