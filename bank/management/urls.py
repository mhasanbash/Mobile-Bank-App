
from django.urls import path
from .views import Home, Profile, Signin, signout, CreatedBankAccount, MakeTransection, account_detail, LastTransections, CalculateLoanPoint, CollectLoan, LoanList,LoanInstallmentList,LoanInstallmentPayment


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
    path('account_turnover/', LastTransections.as_view(), name='account_turnover'),
    path('point/', CalculateLoanPoint.as_view(), name='point'),
    path('collect_loan/', CollectLoan.as_view(), name='collect_loan'),
    path('loan_list/', LoanList.as_view(), name='loan_list'),
    path('installment/', LoanInstallmentList.as_view(), name='installment'),
    path('installment_pay/', LoanInstallmentPayment.as_view(), name='installment_pay')
]