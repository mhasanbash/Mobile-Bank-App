from django.shortcuts import render
from .form import SignInForm, CreateAccForm, MakeTransactionForm, AccountTurnoverForm, LoanPaymentForm
from django.views import View
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date, timedelta

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
                # with connection.cursor() as cursor:
                #     cursor.execute("INSERT INTO BANK_ACCOUNT (user_id, account_number, primary_password, Balance, date_opened, account_status) VALUES (%s, %s, %s, %s, %s, %s)"
                #                 , [request.session['user_id'], data['acc_number'], data['password'], data['balance'] , date_opened, data['acc_status']])
                with connection.cursor() as cursor:  
                    cursor.execute("CALL create_account(%s, %s, %s, %s, %s, %s)", [request.session['user_id'], data['acc_number'], data['password'], data['balance'] , date_opened, data['acc_status']])

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
        form = AccountTurnoverForm()
        return render(request, 'account_turnover.html', {'form':form})
    
    def post(self, request):
        form = AccountTurnoverForm(request.POST)
        if form.is_valid():
            acc_number  = form.cleaned_data['acc_number']
            number  = form.cleaned_data['number']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if (number):
                try : 
                    result=[]
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT last_transactions(%s, %s)' , [acc_number, number])
                        instances = cursor.fetchall()
                        for ins in instances:
                            ins = ins[0]
                            ins = ins[1: len(ins) - 1]
                            ins = ins.split(',')
                            res = {
                                "src_num" : ins[1],
                                "dst_num" : ins[2],
                                "amount" : ins[3],
                                "date" : ins[4]
                            }
                            result.append(res)
                        print("salam",result)
                        return render(request, 'last_transaction.html', {'results': result})

                except Exception as e:
                    return render(request, 'error.html', {'error_message': str(e)})
            else:
                try : 
                    result=[]
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT last_transactions_date(%s, %s, %s)' , [acc_number, start_date, end_date])
                        instances = cursor.fetchall()
                        for ins in instances:
                            ins = ins[0]
                            ins = ins[1: len(ins) - 1]
                            ins = ins.split(',')
                            res = {
                                "src_num" : ins[1],
                                "dst_num" : ins[2],
                                "amount" : ins[3],
                                "date" : ins[4]
                            }
                            result.append(res)
                        print("salam",result)
                        return render(request, 'last_transaction.html', {'results': result})

                except Exception as e:
                    return render(request, 'error.html', {'error_message': str(e)})
        
        else:
            return render(request, 'error.html', {'error_message': 'form in not valid! error!'})


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

                    return render(request, 'seccessful_transfer.html', {'result': result})

            except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})
        else:
            return render(request, 'error.html', {'error_message': 'error!'})
    

class CalculateLoanPoint(View):
    # acc_number
    def get(self, request):
        try : 
            with connection.cursor() as cursor:
                cursor.execute('SELECT acc.account_number, m.min_amount, m.active_loan FROM BANK_ACCOUNT as acc, MINIMUMMONEY as m WHERE acc.user_id = %s and acc.account_number = m.account_number',[request.session['user_id']])
                instances = cursor.fetchall()
                print(instances)
                return render(request, 'point.html', {'results' : instances})
        except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})
        

class CollectLoan(View):
    # acc_number
    def get(self, request):
        try : 
            with connection.cursor() as cursor:
                cursor.execute('SELECT acc.account_number, acc.account_status, m.min_amount, m.active_loan FROM BANK_ACCOUNT as acc, MINIMUMMONEY as m WHERE acc.user_id = %s and acc.account_number = m.account_number',[request.session['user_id']])
                instances = cursor.fetchall()
                return render(request, 'collect_loan.html', {'results' : instances})
        except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})
        
    def post(self, request):
        acc_number = request.POST.get('account_number')
        rate= request.POST.get('score')
        print(acc_number, rate)
        try : 
            with connection.cursor() as cursor:
                today = date.today()
                sql_date = today.strftime('%Y-%m-%d')
                next_year = today + timedelta(days=365)
                sql_enddate = next_year.strftime('%Y-%m-%d')
                cursor.execute('CALL create_loan_and_installments(%s, %s, %s, %s, %s, %s)', [request.session['user_id'],acc_number,rate, sql_date, sql_enddate, 'False'])
                return HttpResponse('successful')
        except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})


class LoanList(View):
    # user_id 
    def get(self, request):
        try : 
            with connection.cursor() as cursor:
                result = []
                cursor.execute('SELECT get_loans(%s)', [request.session['user_id']])
                instances = cursor.fetchall()
                for ins in instances:
                    ins = ins[0]
                    ins = ins[1: len(ins) - 1]
                    ins = ins.split(',')
                    res = {
                        "load_id" : ins[0],
                        "acc_num" : ins[2],
                        "amount" : ins[3],
                        "start_date" : ins[4],
                        "end_date" : ins[5],
                        "status" : ins[6]
                    }
                    result.append(res)
                print(result)
                return render(request, 'loan_list.html', {'results' : result})
        except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})


class LoanInstallmentList(View):
    # Loan id
    def get(self, request):
        return render(request, 'input.html')
    def post(self, request):
        loan_id = request.POST.get('loanid')
        try : 
            result = []
            with connection.cursor() as cursor:
                cursor.execute('SELECT get_installments(%s)', [loan_id])
                instances = cursor.fetchall()
                for ins in instances:
                    ins = ins[0]
                    ins = ins[1: len(ins) - 1]
                    ins = ins.split(',')
                    res = {
                        "installment_id" : ins[0],
                        "load_id" : ins[1],
                        "acc_num" : ins[2],
                        "payment_deadline" : ins[3],
                        "amount" : ins[4],
                        "date_of_payment" : ins[5],
                        "status" : ins[6]
                    }
                    result.append(res)
                print(result)
                sum=0
                for i in result:
                    temp = float(i['amount'])
                    sum = sum + temp
                print(sum)
                
                sum2=0
                for i in result:
                    if i['status'] == 't':
                        temp = float(i['amount'])
                        sum2 = sum2 + temp

                res = {
                    'sum' : sum,
                    'sum2' : sum2,
                }

                return render(request, 'installment.html', {'results' : result, 'res': res})
        except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})

class LoanInstallmentPayment(View):
    # Loan id 
    def get(self, request):
        form = LoanPaymentForm()
        return render(request, 'installment_pay.html', {'form': form})
    
    def post(self, request):
        form = LoanPaymentForm(request.POST)
        if form.is_valid():
            loan_id  = form.cleaned_data['loan_id']
            try :
                with connection.cursor() as cursor:
                    cursor.execute('CALL pay_earliest_installment(%s)', [loan_id])
                    return HttpResponseRedirect(reverse('management:Home'))

            except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})
        else:
            return render(request, 'error.html', {'error_message': form.errors})





