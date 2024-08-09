# Generated by Django 5.0.7 on 2024-08-09 12:13

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
            name='Client',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.user')),
                ('preferences', models.JSONField(default=dict)),
                ('client_status', models.CharField(choices=[('new', 'New'), ('loyal', 'Loyal'), ('regular', 'Regular')], default='new', max_length=20)),
                ('tags', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='property_listing.realestateagent')),
            ],
            bases=('core.user',),
        ),
        migrations.CreateModel(
            name='ClientAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engagement_metrics', models.JSONField(default=dict)),
                ('client_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='client_management.client')),
            ],
        ),
        migrations.CreateModel(
            name='ClientRealEstateAgent',
            fields=[
                ('realestateagent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='property_listing.realestateagent')),
                ('clients', models.ManyToManyField(related_name='agents', to='client_management.client')),
            ],
            bases=('property_listing.realestateagent',),
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('clientinteraction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.clientinteraction')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_listing.realestateagent')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client_management.client')),
            ],
            bases=('core.clientinteraction',),
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('task', models.TextField()),
                ('due_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_listing.realestateagent')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client_management.client')),
            ],
        ),
    ]
