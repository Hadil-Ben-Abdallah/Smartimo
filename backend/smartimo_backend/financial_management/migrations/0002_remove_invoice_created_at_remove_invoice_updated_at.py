# Generated by Django 5.0.7 on 2024-08-28 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='updated_at',
        ),
    ]