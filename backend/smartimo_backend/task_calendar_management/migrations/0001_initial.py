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
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('type', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('details', models.TextField()),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_agent', to='property_listing.realestateagent')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_client', to='core.user')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
            ],
        ),
        migrations.CreateModel(
            name='CalendarIntegration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_service', models.CharField(max_length=50)),
                ('sync_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=50)),
                ('last_sync', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('topic', models.CharField(max_length=255)),
                ('agenda', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=50)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings_organized', to='core.user')),
                ('participants', models.ManyToManyField(related_name='meetings_participated', to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('checklist', models.JSONField()),
                ('status', models.CharField(max_length=50)),
                ('report', models.FileField(blank=True, null=True, upload_to='inspection_reports/')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspections', to='core.user')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=50)),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=50)),
                ('category', models.CharField(choices=[('sales', 'Sales'), ('rental', 'Rental'), ('maintenance', 'Maintenance')], default='sales', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='TaskManager',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('calendar', models.JSONField(default=dict)),
                ('reminders', models.JSONField(default=list)),
                ('tasks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_calendar_management.task')),
            ],
        ),
    ]
