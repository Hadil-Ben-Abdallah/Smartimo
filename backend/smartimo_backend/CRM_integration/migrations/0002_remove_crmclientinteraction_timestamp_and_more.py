# Generated by Django 5.0.7 on 2024-08-28 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CRM_integration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crmclientinteraction',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='crmclientsync',
            name='last_update_time',
        ),
    ]
