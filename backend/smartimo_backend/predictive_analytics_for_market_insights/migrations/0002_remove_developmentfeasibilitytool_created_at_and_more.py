# Generated by Django 5.0.7 on 2024-08-28 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictive_analytics_for_market_insights', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developmentfeasibilitytool',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='developmentfeasibilitytool',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='investmentdashboard',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='investmentdashboard',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='markettrendanalysis',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='markettrendanalysis',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='predictiveanalytics',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='predictiveanalytics',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='propertyvaluationmodel',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='propertyvaluationmodel',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='rentaldemandforecast',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='rentaldemandforecast',
            name='updated_at',
        ),
    ]
