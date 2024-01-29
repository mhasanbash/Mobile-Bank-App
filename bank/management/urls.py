
from django.urls import path
from .views import Home, Profile, Signin, signout, CreatedBankAccount

app_name = 'management'

urlpatterns = [
    path('Home/', Home.as_view(), name='Home'),
    path('profile/', Profile.as_view(), name='profile'),
    path('signin/', Signin.as_view(), name='signin'),
    path('signout/', signout, name='signout'),
    path('createacc/', CreatedBankAccount.as_view(), name='created_bank_account'),
]