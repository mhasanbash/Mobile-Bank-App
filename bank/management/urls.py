
from django.urls import path
from .views import Home, Profile, Signin, signout, CreatedBankAccount, MakeTransection, account_detail

app_name = 'management'

urlpatterns = [
    path('Home/', Home.as_view(), name='Home'),
    path('profile/', Profile.as_view(), name='profile'),
    path('signin/', Signin.as_view(), name='signin'),
    path('signout/', signout, name='signout'),
    path('createacc/', CreatedBankAccount.as_view(), name='created_bank_account'),
    path('transfer/', MakeTransection.as_view(), name='MakeTransection'),
    path('accountdetail/', account_detail, name='accountdetail'),
    path('successful/', account_detail, name='successful'),
    path('account_turnover/', account_detail, name='account_turnover'),
]