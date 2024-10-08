# Generated by Django 5.0.7 on 2024-08-20 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('lease_rental_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('issue_type', models.CharField(max_length=255)),
                ('severity', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('photos', models.JSONField(default=list)),
                ('urgency_level', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=50)),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='submitted', max_length=50)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('completion_date', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to='lease_rental_management.propertymanager')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='core.property')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_requests', to='lease_rental_management.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenancePropertyManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_managers', to='lease_rental_management.propertymanager')),
                ('assigned_requests', models.ManyToManyField(related_name='assigned_requests', to='maintenance_and_service_requests.maintenancerequest')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceTechnician',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('skills', models.TextField()),
                ('assigned_tasks', models.ManyToManyField(related_name='technicians', to='maintenance_and_service_requests.maintenancerequest')),
            ],
        ),
        migrations.CreateModel(
            name='TenantRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_number', models.CharField(max_length=50)),
                ('maintenance_requests', models.ManyToManyField(related_name='tenant_requests', to='maintenance_and_service_requests.maintenancerequest')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_requests', to='lease_rental_management.tenant')),
            ],
        ),
    ]
