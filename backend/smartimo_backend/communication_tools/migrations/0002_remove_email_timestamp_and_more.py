# Generated by Django 5.0.7 on 2024-08-28 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication_tools', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='instantmessage',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='smsnotification',
            name='timestamp',
        ),
    ]