# Generated by Django 5.0.7 on 2024-08-17 11:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0006_feedback'),
        ('lease_rental_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntegrationPropertyManager',
            fields=[
                ('propertymanager_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lease_rental_management.propertymanager')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=('lease_rental_management.propertymanager',),
        ),
        migrations.CreateModel(
            name='IntegrationFinancialReport',
            fields=[
                ('financialreport_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.financialreport')),
                ('report_type', models.CharField(choices=[('profit_and_loss_statement', 'Profit and Loss Statement'), ('balance_sheet', 'Balance Sheet'), ('cash_flow_summary', 'Cash Flow Summary')], default='profit_and_loss_statement', max_length=255)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
            ],
            bases=('core.financialreport',),
        ),
        migrations.CreateModel(
            name='Export',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('export_type', models.CharField(choices=[('financial_data', 'Financial Data'), ('transaction_records', 'Transaction Records')], max_length=255)),
                ('export_format', models.CharField(choices=[('csv', 'CSV'), ('excel', 'Excel'), ('xml', 'XML')], default='csv', max_length=50)),
                ('date_range', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integration_with_accounting_software.integrationpropertymanager')),
            ],
        ),
        migrations.CreateModel(
            name='IntegrationSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('accounting_software', models.CharField(choices=[('quickBooks', 'QuickBooks'), ('xero', 'Xero'), ('freshBooks', 'FreshBooks')], default='quickBooks', max_length=255)),
                ('sync_frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('on_demand', 'On-demand')], default='weekly', max_length=255)),
                ('data_mapping_rules', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integration_with_accounting_software.integrationpropertymanager')),
            ],
        ),
        migrations.CreateModel(
            name='Reconciliation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_transactions', models.JSONField()),
                ('ledger_entries', models.JSONField()),
                ('reconciliation_date', models.DateField()),
                ('discrepancies', models.JSONField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('flagged', 'Flagged')], default='pending', max_length=255)),
                ('property_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integration_with_accounting_software.integrationpropertymanager')),
            ],
        ),
    ]
