from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View
from django.http.response import HttpResponse
from .forms import *
from .models import *
import datetime
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm,SetPasswordForm
from django.views.generic import CreateView
from django.contrib.auth import authenticate,login,logout,get_user_model

# Create your views here.
current_date = datetime.date.today()

def totalexp(amount,id):
    total = 0
    for amt in amount:
        total += amt.dailyexp
    total = round(total,2)
    if total != 0:
        month_total = MonthReport.objects.filter(id = id).update(total=total)
    return total

login_required(login_url='login')
def monthlyReport(request):
    user = User.objects.get(username = request.user)
    month = request.GET.get('month') or ''
    print(month)
    if month:
        month = month.split('-')
        year,month = month[0],month[1]
    try:
        sal = MonthReport.objects.get(month__month__icontains=current_date.month,month__year=current_date.year,user=user.id)
        if month: sal = MonthReport.objects.get(month__month=month,month__year=year)
        form = MonthReportForm(instance=sal)
        expdetails = DailyExpenses.objects.filter(month_report=sal.id)
        total = totalexp(expdetails,sal.id)
        context = {'expdetails':expdetails,'sal':sal,'form':form,'total':total}
        return render(request,'home.html',context)
    except MonthReport.DoesNotExist:
        print('record does not exist')
        # d = current_date.replace(day=1)
        # last_month = d - datetime.timedelta(days=1)
        if not Month.objects.filter(month__icontains=current_date.month,year=current_date.year).exists():
            month = Month.objects.create(month='0'+str(current_date.month),year=current_date.year)
            month.save()
        else:
            month = Month.objects.get(month__icontains=current_date.month,year=current_date.year)
        if not Month.objects.filter(month=month,year=current_date.year).exists():
            month = Month.objects.create(month=month,year=current_date.year)
            month.save()
        sal = MonthReport.objects.create(salary=0,month=month,currency='Rs.',total=0,user=user)

        sal.save()
        expdetails = DailyExpenses.objects.filter(month_report=sal.id)
        form = MonthReportForm(instance=sal)
        total = totalexp(expdetails,sal.id)
        context = {'expdetails':expdetails,'sal':sal,'form':form,'total':total}
        return render(request,'home.html',context)

class ChartView(View):
    template_name = 'expchart.html'
    def get(self,request):
        user = User.objects.get(username = request.user)
        month = MonthReport.objects.filter(user = user.id,month__year = current_date.year)
        monthdict = {}
        monthlist = []
        for sal in month: monthdict[int(sal.month.month)]=sal.total
        for i in range(1,13):
            if i in monthdict.keys(): monthlist.append(monthdict[i])
            else: monthlist.append(0)
        
        return render(request,self.template_name,{'month':monthlist,'year':current_date.year})

class LoginView(View):
    template_name = 'login.html'
    form = AuthenticationForm()

    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/home/')
        return render(request,self.template_name,{'form':self.form})
    
    def post(self,request):
        form = AuthenticationForm(request=request,data = request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    return redirect('/home/')
                else:
                    messages.error(request,'Invalid username or password.')
            else:
                messages.error(request,'Invalid username or password.')
        except Exception as e:
            print(e)
        form = self.form
        return render(request,self.template_name,{'form':self.form})
    
class SignupView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def logoutView(request):
    logout(request)
    return redirect('/')

# @user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = User.objects.filter(email = user_email).first()
            subject = "Password Reset request"
            message = render_to_string("template_reset_password.html",{
                'user':associated_user,
                'domain':get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                'token': account_activation_token.make_token(associated_user),
                "protocol": 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(subject,message,to=[associated_user.email])
            if email.send():
                messages.success(request,"""
                <p>
                    We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                    You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                    you registered with, and check your spam folder.
                </p>
                """)
            else:
                messages.error(request,"Problem sending reset password email <b>SERVER PROBLME</b>")
        return redirect('home')
    form = PasswordResetForm()

    return render(request=request,template_name="password_reset.html",context={"form":form})

def passwordResetConfirm(request,uidb64,token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_encode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Your password has been set')
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)

        form = SetPasswordForm(user)
        return render(request,'password_reset_confirmation.html',{'form':form})
    else:
        messages.error(request,'Link is expired')
    
    messages.error(request,'Something went wrong, redirecting to home page')
    return redirect('login')

    return redirect('home')

class DailyExpensesView(View):
    template_name = "monthlyexpense.html"

    def get(self,request,id):
        month = MonthReport.objects.get(id = id)
        monthlyexp = DailyExpensesForm()
        context = {'form':monthlyexp,'month':month}
        return render(request,self.template_name,context)
    
    def post(self,request,id):
        month = MonthReport.objects.get(id = id)
        monthlyexp = DailyExpensesForm(data=request.POST)
        context = {'form':monthlyexp,'month':month}

        try:
            if monthlyexp.is_valid():
                fm = monthlyexp.save(commit = False)
                fm.month_report = month
                fm.date = timezone.now()
                fm.save()
            else:
                print(monthlyexp.errors)
        except Exception as e:
            print(e)       

        return render(request,self.template_name,context)    

class UpdateSalaryView(View):
    template_name = "updatesalary.html"
    def get(self,request,id):
        month = MonthReport.objects.get(id = id)
        form = MonthReportForm(instance=month)
        return render(request,self.template_name,{'form':form})

    def post(self,request,id):
        month = MonthReport.objects.get(id = id)
        form = MonthReportForm(request.POST,instance=month)
        if form.is_valid():
            form.save()
        return render(request,self.template_name,{'form':form})
    
class UpdateExpenseView(View):
    template_name = "updateexpense.html"
    def get(self,request,id):
        daily = DailyExpenses.objects.get(id=id)
        form = DailyExpensesForm(instance=daily)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,id):
        daily = DailyExpenses.objects.get(id=id)
        form = DailyExpensesForm(request.POST,instance=daily)
        if form.is_valid():
            form.save()
        return render(request,self.template_name,{'form':form})
    
def deleteExpView(request,id):
    daily = DailyExpenses.objects.get(id = id)
    if request.method == 'POST':
        daily.delete()
    return render(request,'deleteexpense.html')