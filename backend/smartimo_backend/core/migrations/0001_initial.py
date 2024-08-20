# Generated by Django 5.0.7 on 2024-08-20 00:32

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientInteraction',
            fields=[
                ('client_interaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('interaction_type', models.CharField(max_length=50)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('communication_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField()),
                ('comments', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('status', models.CharField(max_length=50)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Portal',
            fields=[
                ('portal_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=50)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('property_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('residential', 'Residential'), ('commercial', 'Commercial'), ('mixed_use', 'Mixed Use'), ('land', 'Land'), ('special_purpose', 'Special Purpose'), ('investment', 'Investment'), ('luxury', 'Luxury'), ('recreational', 'Recreational'), ('development', 'Development')], default='residential', max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('photos', models.ImageField(upload_to='photos/')),
                ('videos', models.FileField(upload_to='videos/')),
                ('size', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bathroom_number', models.IntegerField(default=0)),
                ('badroom_number', models.IntegerField(default=0)),
                ('garage', models.BooleanField(default=False)),
                ('garden', models.BooleanField(default=False)),
                ('swiming_pool', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('year_built', models.DateField(auto_now=True)),
                ('status', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('reminder_id', models.AutoField(primary_key=True, serialize=False)),
                ('message_content', models.TextField()),
                ('reminder_date', models.DateTimeField()),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quartly', 'Quartly'), ('bi-annually', 'Bi-annually'), ('annually', 'Annually')], default='daily', max_length=50)),
                ('delivary_channel', models.CharField(choices=[('email', 'Email'), ('sms', 'SMS'), ('in_platform_alert', 'In-platform Alert')], default='email', max_length=50)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('sent', 'Sent')], default='scheduled', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('data', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('contact_info', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SalesOpportunity',
            fields=[
                ('sales_opportunity_id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cin', models.CharField(max_length=8)),
                ('birth_date', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=250)),
                ('credit_card_number', models.CharField(max_length=20)),
                ('job_title', models.CharField(max_length=100)),
                ('user_type', models.CharField(choices=[('client', 'Client'), ('lease_rental_tenant', 'Lease Rental Tenant'), ('property_owner', 'Property Owner'), ('property_manager', 'Property Manager'), ('inspector', 'Inspector'), ('vendor', 'Vendor'), ('prospective_buyer_renter', 'Prospective Buyer Renter'), ('real_estate_agent', 'Real Estate Agent'), ('real_estate_developer', 'Real Estate Developer'), ('prospective_tenant', 'Prospective Tenant')], default='client', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('document_type', models.CharField(choices=[('contract', 'Contract'), ('agreement', 'Agreement'), ('deed', 'Deed'), ('lease', 'Lease'), ('addendum', 'Addentum'), ('inspection_report', 'Inspection Report'), ('insurance_policy', 'Insurance Policy')], default='contract', max_length=50)),
                ('file_path', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('version', models.CharField(max_length=10)),
                ('access_permissions', models.JSONField(default=dict)),
                ('expiration_date', models.DateField()),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
    ]
