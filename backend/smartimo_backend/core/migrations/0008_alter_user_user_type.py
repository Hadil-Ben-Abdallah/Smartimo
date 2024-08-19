# Generated by Django 5.0.7 on 2024-08-19 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('client', 'Client'), ('lease_rental_tenant', 'Lease Rental Tenant'), ('property_owner', 'Property Owner'), ('property_manager', 'Property Manager'), ('inspector', 'Inspector'), ('vendor', 'Vendor'), ('prospective_buyer_renter', 'Prospective Buyer Renter'), ('real_estate_agent', 'Real Estate Agent'), ('real_estate_developer', 'Real Estate Developer'), ('prospective_tenant', 'Prospective Tenant')], default='client', max_length=50),
        ),
    ]
