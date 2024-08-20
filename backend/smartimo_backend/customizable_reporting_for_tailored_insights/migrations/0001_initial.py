# Generated by Django 5.0.7 on 2024-08-20 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('lease_rental_management', '0001_initial'),
        ('property_listing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplianceReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.report')),
                ('template', models.TextField()),
                ('fields', models.CharField(choices=[('regulatory_requirements', 'Regulatory Requirements'), ('audit findings', 'Audit Findings'), (' compliance_status', 'Compliance Status')], default='regulatory_requirements', max_length=100)),
                ('filters', models.CharField(choices=[('regulation', 'Regulation'), ('property', 'Property')], default='property', max_length=100)),
            ],
            bases=('core.report',),
        ),
        migrations.CreateModel(
            name='InvestmentReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.report')),
                ('fields', models.CharField(choices=[('property_performance', 'Property Performance'), ('market_trends', 'Market Trends'), (' investment_metrics', 'Investment Metrics')], default='property_performance', max_length=100)),
                ('filters', models.CharField(choices=[('property', 'Property'), ('market', 'Market'), ('metrics', 'Metrics')], default='property', max_length=100)),
                ('external_data_sources', models.JSONField()),
            ],
            bases=('core.report',),
        ),
        migrations.CreateModel(
            name='CustomizableFinancialReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.report')),
                ('filters', models.CharField(choices=[('property', 'Property'), ('timeframe', 'Timeframe')], default='property', max_length=100)),
                ('groupings', models.JSONField()),
                ('sort_options', models.JSONField()),
                ('property_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_listing.propertyowner')),
            ],
            bases=('core.report',),
        ),
        migrations.CreateModel(
            name='MaintenanceReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.report')),
                ('fields', models.CharField(choices=[('service_requests', 'Service Requests'), ('work_orders', 'Work Orders'), (' vendor_performance', 'Vendor Performance')], default='listings', max_length=100)),
                ('filters', models.CharField(choices=[('location', 'Location'), ('category', 'Category'), ('urgency', 'Urgency')], default='location', max_length=100)),
                ('dashboard', models.JSONField()),
                ('property_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lease_rental_management.propertymanager')),
            ],
            bases=('core.report',),
        ),
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.report')),
                ('template', models.TextField()),
                ('fields', models.CharField(choices=[('listings', 'Listings'), ('leads', 'Leads'), (' transactions', ' Transactions')], default='listings', max_length=100)),
                ('filters', models.CharField(choices=[('listing', 'Listing'), ('timeframe', 'Timeframe')], default='listing', max_length=100)),
                ('visualizations', models.JSONField()),
                ('real_estate_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_listing.realestateagent')),
            ],
            bases=('core.report',),
        ),
    ]
