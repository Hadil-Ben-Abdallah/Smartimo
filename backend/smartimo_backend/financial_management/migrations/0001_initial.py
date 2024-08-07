# Generated by Django 5.0.7 on 2024-08-07 08:46

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('unpaid', 'Unpaid'), ('paid', 'Paid'), ('overdue', 'Overdue')], max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('itemized_charges', models.JSONField()),
                ('payment_instructions', models.TextField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('credit_card_number', models.CharField(max_length=20)),
                ('reached_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remaining_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('payment_method', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('processed', 'Processed'), ('pending', 'Pending')], max_length=20)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_management.invoice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='TenantPortal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invoices', models.ManyToManyField(to='financial_management.invoice')),
                ('payment_history', models.ManyToManyField(to='financial_management.payment')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='TheFinancialReport',
            fields=[
                ('financialreport_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.financialreport')),
                ('report_type', models.CharField(max_length=50)),
                ('report_period', models.CharField(max_length=50)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
            ],
            bases=('core.financialreport',),
        ),
    ]
