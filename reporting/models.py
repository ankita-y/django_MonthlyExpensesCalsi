from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Month(models.Model):
    month_choice = (
    ('01','January'),('02','February'),('03','March'),('04','April'),
    ('05','May'),('06','June'),('07','July'),('08','August'),
    ('09','September'),('10','October'),('11','November'),('12','December')
    )
    month = models.CharField(max_length=20,choices=month_choice)
    year = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class MonthReport(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    month = models.ForeignKey(Month,on_delete=models.CASCADE)
    salary = models.FloatField(null=True)
    currency = models.CharField(max_length=10,default='Rs.')
    total = models.FloatField(null = True)

    def __str__(self):
        return str(self.id)


class DailyExpenses(models.Model):
    month_report = models.ForeignKey(MonthReport, on_delete=models.CASCADE)
    dailyexp = models.FloatField()
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=500,null=True,blank=True)
    date = models.DateTimeField(auto_created=True,null=False)  
    paymentmethod = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.title)[:100]