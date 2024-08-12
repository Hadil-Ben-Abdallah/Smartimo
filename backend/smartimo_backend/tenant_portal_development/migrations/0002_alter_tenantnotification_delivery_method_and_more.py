# Generated by Django 5.0.7 on 2024-08-12 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_portal_development', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantnotification',
            name='delivery_method',
            field=models.CharField(choices=[('email', 'Email'), ('sms', 'SMS')], default='email', max_length=50),
        ),
        migrations.AlterField(
            model_name='tenantnotification',
            name='type',
            field=models.CharField(choices=[('lease_renewal', 'Lease Renewal'), ('rent_increase', 'Rent Increase')], default='lease_renewal', max_length=255),
        ),
    ]