# Generated by Django 5.0.7 on 2024-08-20 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('property_listing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('visit_purpose', models.CharField(choices=[('viewing', 'Viewing'), ('inspecting', 'Inspecting')], default='viewing', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisitorNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notification')),
                ('type', models.CharField(choices=[('reminder', 'Reminder'), ('alert', 'Alert')], default='reminder', max_length=50)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitor_management_for_property_access.visitor')),
            ],
            bases=('core.notification',),
        ),
        migrations.CreateModel(
            name='VisitorProperty',
            fields=[
                ('property_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.property')),
                ('listing_type', models.CharField(choices=[('rental', 'Rental'), ('sale', 'Sale')], default='rental', max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_listing.propertyowner')),
            ],
            bases=('core.property',),
        ),
        migrations.CreateModel(
            name='VisitorFeedback',
            fields=[
                ('feedback_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.feedback')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitor_management_for_property_access.visitor')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitor_management_for_property_access.visitorproperty')),
            ],
            bases=('core.feedback',),
        ),
        migrations.CreateModel(
            name='Showing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_listing.realestateagent')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitor_management_for_property_access.visitor')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitor_management_for_property_access.visitorproperty')),
            ],
        ),
        migrations.CreateModel(
            name='AccessControl',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('access_code', models.CharField(max_length=50)),
                ('access_start', models.DateTimeField()),
                ('access_end', models.DateTimeField()),
                ('permissions', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitor_management_for_property_access.visitor')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitor_management_for_property_access.visitorproperty')),
            ],
        ),
    ]
