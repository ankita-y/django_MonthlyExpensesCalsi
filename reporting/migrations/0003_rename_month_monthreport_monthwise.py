# Generated by Django 4.0.3 on 2023-03-11 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_month_remove_monthreport_year_monthreport_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthreport',
            old_name='month',
            new_name='monthwise',
        ),
    ]
