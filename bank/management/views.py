from django.shortcuts import render
from .form import SignInForm
# Create your views here.
from django.views import View
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.urls import reverse

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



#_________________________________________________________________________________________________ 
class Signin(View):
    # username and password
    def get(self, request):
        form = SignInForm()
        form.fields['username'].widget.attrs.update({'class': 'form-control'})
        form.fields['password'].widget.attrs.update({'class': 'form-control'}) 
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
                    if instances:
                        request.session['username'] = instances[0][1]
                        request.session['password'] = instances[0][2]
                        request.session['first_name'] = instances[0][3]
                        request.session['last_name'] = instances[0][4]
                        request.session['address'] = instances[0][5]
                        request.session['phonenumber'] = instances[0][6]
                        request.session['email'] = instances[0][7]
                        request.session['date_joined'] = instances[0][8]
                        request.session['is_superuser'] = instances[0][9]
                    return HttpResponseRedirect(reverse('management:Home'))

            except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})

        else:
            return render(request, 'error.html', {'error_message': 'فرم ورود معتبر نیست'})
            # return render(request, 'home.html')


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('management:signin'))

#________________________________________________________________________________________________________


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





