from django.shortcuts import render
from .form import SignInForm
# Create your views here.
from django.views import View
from django.http import HttpResponse
from django.db import connection

class Home(View):
    def get(self, request):
        # کد برای پردازش درخواست GET
         return render(request, "home.html")

    def post(self, request):
        # کد برای پردازش درخواست POST
        return HttpResponse("This is a POST response")

class Profile(View):
    def get(self, request):
        # کد برای پردازش درخواست GET
         return render(request, "profile.html")

    def post(self, request):
        # کد برای پردازش درخواست POST
        return HttpResponse("This is a POST response")
    
class Signin(View):
    # username and password
    def get(self, request):
        form = SignInForm()
        form.fields['username'].widget.attrs.update({'class': 'form-control'})  # اضافه کردن کلاس CSS به فیلد username
        form.fields['password'].widget.attrs.update({'class': 'form-control'})  # اضافه کردن کلاس CSS به فیلد password
        return render(request, "signin.html", {'form': form})
    
    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try : 
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM USERS WHERE username = %s and password = %s", [username, password])
                    instances = cursor.fetchall()
                    return HttpResponse(instances)

            except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})

        else:
            return render(request, 'error.html', {'error_message': 'فرم ورود معتبر نیست'})
            # return render(request, 'home.html')

class changePassword(View):
    # user id and old_pass and new_pass
    pass

class AccountDetail(View):
    # user id
    pass

class LastTransections(View):
    # acc_number and number
    pass

class LastTransectionsDate(View):
    # acc_number and start date and end date
    pass

class AccountDetail(View):
    # acc_number
    pass

class AccountOwner(View):
    # acc_number
    pass

class BlockAccount(View):
    # acc_number
    pass

class MakeTransection(View):
    # source acc_num and dest acc_num and amount
    pass

class CalculateLoanPoint(View):
    # acc_number
    pass

class CollectLoan(View):
    # acc_number
    pass

class LoanList(View):
    # user_id 
    pass

class LoanInstallmentList(View):
    # Loan id
    pass

class LoanInstallmentPayment(View):
    # Loan id 
    pass





