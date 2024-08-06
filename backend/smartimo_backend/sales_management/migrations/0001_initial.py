# Generated by Django 5.0.7 on 2024-08-06 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client_management', '0001_initial'),
        ('core', '0001_initial'),
        ('property_listing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('client_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='client_management.client')),
                ('lead_source', models.CharField(choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('search_web', 'Search Web'), ('tik_tok', 'Tik Tok')], default='search_web', max_length=50)),
                ('lead_status', models.CharField(choices=[('new', 'New'), ('contacted', 'Contacted'), ('qualified', 'Qualified')], max_length=50)),
                ('property_type', models.CharField(choices=[('house', 'House'), ('office', 'Office'), ('apartment', 'Apartment')], default='house', max_length=50)),
                ('note', models.TextField(max_length=2000)),
            ],
            bases=('client_management.client',),
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('start_date', models.DateField(auto_now=True)),
                ('end_date', models.DateField(auto_now=True)),
                ('content_of_deal', models.TextField(max_length=2000)),
                ('description', models.TextField(max_length=2000)),
                ('is_approved', models.BooleanField(default=False)),
                ('deal_type', models.CharField(choices=[('rent', 'Rent'), ('sell', 'Sell')], default='rent')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales_management.lead')),
            ],
        ),
        migrations.CreateModel(
            name='SalesAnalytics',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('metrics', models.JSONField()),
                ('report_type', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_listing.realestateagent')),
            ],
        ),
        migrations.CreateModel(
            name='SalesClientInteraction',
            fields=[
                ('interaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='client_management.interaction')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales_management.lead')),
            ],
            bases=('client_management.interaction',),
        ),
        migrations.CreateModel(
            name='SalesPipeline',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stages', models.JSONField()),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_listing.realestateagent')),
            ],
        ),
        migrations.CreateModel(
            name='TheSalesOpportunity',
            fields=[
                ('salesopportunity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.salesopportunity')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales_management.lead')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
            ],
            bases=('core.salesopportunity',),
        ),
        migrations.CreateModel(
            name='Collaboration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('notes', models.TextField()),
                ('assigned_tasks', models.JSONField()),
                ('activity_feed', models.JSONField()),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_listing.realestateagent')),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales_management.thesalesopportunity')),
            ],
        ),
    ]
