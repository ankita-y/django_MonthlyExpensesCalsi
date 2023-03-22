# Generated by Django 4.0.3 on 2023-03-05 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.FloatField(null=True)),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('currency', models.CharField(default='Rs.', max_length=10)),
                ('total', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True)),
                ('dailyexp', models.FloatField()),
                ('title', models.CharField(max_length=200)),
                ('desc', models.CharField(blank=True, max_length=500, null=True)),
                ('paymentmethod', models.CharField(blank=True, max_length=100, null=True)),
                ('month_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.monthreport')),
            ],
        ),
    ]