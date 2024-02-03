from django.shortcuts import render
from .form import SignInForm, CreateAccForm, MakeTransactionForm
from django.views import View
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse

class Home(View):
    def get(self, request):
        # کد برای پردازش درخواست GET
         #یک کوئری برای برای دریافت حساب های یک شخص با user id
        try : 
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM BANK_ACCOUNT WHERE user_id = %s", [request.session["user_id"]])
                instances = cursor.fetchall()
                # for i in instances:

                print(instances)
                return render(request, "home.html", {'accounts' : instances})
            
        except Exception as e:
            return render(request, 'error.html', {'error_message': str(e)})
        

class Profile(View):
    def get(self, request):
        # کد برای پردازش درخواست GET
        return render(request, "profile.html", )

    def post(self, request):
        # کد برای پردازش درخواست POST
        return HttpResponse("This is a POST response")


class CreatedBankAccount(View):
    def get(self, request):
        form = CreateAccForm()
        form.fields['owner'].initial = request.session['first_name'] + ' ' + request.session['last_name']
        return render(request, "create_acc.html", {'form':form})

    def post(self, request):
        form = CreateAccForm(request.POST)
        if form.is_valid():
            
            data = form.cleaned_data
            date_opened = data['date_open'].strftime('%Y-%m-%d')
            print(request.session['user_id'], data['acc_number'], data['password'], data['balance'], 0 , date_opened, data['acc_status'])
            try : 
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO BANK_ACCOUNT (user_id, account_number, primary_password, Balance, date_opened, account_status) VALUES (%s, %s, %s, %s, %s, %s)"
                                , [request.session['user_id'], data['acc_number'], data['password'], data['balance'] , date_opened, data['acc_status']])
                    
            except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})
            
            return HttpResponseRedirect(reverse('management:Home'))
        
        else:
            return render(request, 'error.html', {'error_message': form.errors})


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
                        request.session['user_id'] = instances[0][0]
                        request.session['username'] = instances[0][1]
                        request.session['password'] = instances[0][2]
                        request.session['first_name'] = instances[0][3]
                        request.session['last_name'] = instances[0][4]
                        request.session['address'] = instances[0][5]
                        request.session['phonenumber'] = instances[0][6]
                        request.session['email'] = instances[0][7]
                        request.session['date_joined'] = instances[0][8].isoformat()
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


class changePassword(View):
    # user id and old_pass and new_pass
    pass


class AccountDetail(View):
    # user id
    pass


class LastTransections(View):
    # acc_number and number
    def get(self, request):
        pass


class LastTransectionsDate(View):
    # acc_number and start date and end date
    pass

def account_detail(request):
    response = ""
    if request.method == 'GET':
            account_number = request.GET['account_number']
            print(account_number)
            try : 
                with connection.cursor() as cursor:
                    cursor.execute("SELECT usr.first_name , usr.last_name FROM BANK_ACCOUNT as acc, USERS as usr WHERE acc.account_number = %s and acc.user_id = usr.id", [account_number])
                    instances = cursor.fetchall()
                    response = instances[0][0] + " " + instances[0][1]    
            except Exception as e:
                response = "شماره حساب اشتباه است"
    return HttpResponse(response)



class AccountOwner(View):
    # acc_number
    pass

class BlockAccount(View):
    # acc_number
    pass

class MakeTransection(View):
    # source acc_num and dest acc_num and amount
    def get(self, request):
        form = MakeTransactionForm()
        return render(request, 'moneytransfer.html', {'form' : form})
    
    def post(self, request):
        form = MakeTransactionForm(request.POST)
        if form.is_valid():

            source_account  = form.cleaned_data['src_account_number']
            destination_account  = form.cleaned_data['dst_account_number']
            amount = form.cleaned_data['amount']
            password = form.cleaned_data['password']
            
            try : 
                with connection.cursor() as cursor:
                    cursor.execute('SELECT transfer_fund(%s, %s, %s, %s)' , [source_account, destination_account, amount, password])
                    instances = cursor.fetchall()
                    res = instances[0][0]
                    res = res[1: len(res) - 1]
                    res = res.split(',')
                    result = {
                        "src_num" : res[1],
                        "dst_num" : res[2],
                        "amount" : res[3],
                    }
                    print(tuple(res))

                    return render(request, 'seccessful_transfer.html', {'result': result})

            except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})
        else:
            return render(request, 'error.html', {'error_message': 'error!'})
    

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





