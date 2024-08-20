# Generated by Django 5.0.7 on 2024-08-20 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticsReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.report')),
                ('type', models.CharField(choices=[('property_performance', 'Property Performance'), ('sales_trend', 'Sales Trend'), ('financial_performance', 'Financial Performance'), ('client_engagement', 'Client Engagement')], default='property_performance', max_length=50)),
                ('filters', models.JSONField(default=dict)),
                ('visualizations', models.JSONField(default=list)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
            bases=('core.report',),
        ),
        migrations.CreateModel(
            name='ClientEngagementReport',
            fields=[
                ('analyticsreport_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reporting_and_analytics.analyticsreport')),
                ('lead_conversion_rate', models.FloatField()),
                ('inquiry_response_time', models.FloatField()),
                ('client_satisfaction_score', models.FloatField()),
            ],
            bases=('reporting_and_analytics.analyticsreport',),
        ),
        migrations.CreateModel(
            name='FinancialPerformanceReport',
            fields=[
                ('analyticsreport_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reporting_and_analytics.analyticsreport')),
                ('rental_income', models.FloatField()),
                ('operating_expenses', models.FloatField()),
                ('cash_flow', models.FloatField()),
                ('roi', models.FloatField()),
            ],
            bases=('reporting_and_analytics.analyticsreport',),
        ),
        migrations.CreateModel(
            name='PropertyPerformanceReport',
            fields=[
                ('analyticsreport_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reporting_and_analytics.analyticsreport')),
                ('occupancy_rate', models.FloatField()),
                ('average_rental_income', models.FloatField()),
                ('vacancy_rate', models.FloatField()),
                ('maintenance_costs', models.FloatField()),
                ('noi', models.FloatField()),
            ],
            bases=('reporting_and_analytics.analyticsreport',),
        ),
        migrations.CreateModel(
            name='SalesTrendReport',
            fields=[
                ('analyticsreport_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reporting_and_analytics.analyticsreport')),
                ('sales_volume', models.FloatField()),
                ('average_selling_price', models.FloatField()),
                ('time_on_market', models.FloatField()),
                ('regional_sales_distribution', models.JSONField(default=dict)),
            ],
            bases=('reporting_and_analytics.analyticsreport',),
        ),
        migrations.CreateModel(
            name='AutomatedReportScheduler',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily', max_length=50)),
                ('recipients', models.JSONField(default=list)),
                ('delivery_channel', models.CharField(max_length=50)),
                ('last_run', models.DateTimeField(blank=True, null=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting_and_analytics.analyticsreport')),
            ],
        ),
    ]
