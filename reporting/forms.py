from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm

month_choice = [
    (1,'January'),(2,'February'),(3,'March'),(4,'April'),
    (5,'May'),(6,'June'),(7,'July'),(8,'August'),
    (9,'September'),(10,'October'),(11,'November'),(12,'December')
    ]


class MonthReportForm(forms.ModelForm):
    
    class Meta:
        model = MonthReport
        fields = ['salary','currency']

class DailyExpensesForm(forms.ModelForm):
    class Meta:
        model = DailyExpenses
        fields = ['dailyexp','title','desc','paymentmethod']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self,*args,**kwargs):
        super(PasswordResetForm,self).__init__(*args,kwargs)
