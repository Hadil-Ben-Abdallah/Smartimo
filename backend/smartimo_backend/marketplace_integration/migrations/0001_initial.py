# Generated by Django 5.0.7 on 2024-08-09 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketplacePropertyListing',
            fields=[
                ('property_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.property')),
                ('marketplace_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
            bases=('core.property',),
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('availability_dates', models.JSONField(default=list)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(default='pending', max_length=50)),
                ('marketplace_booking_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=50)),
                ('marketplace_transaction_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('marketplace_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marketplace_transactions', to='marketplace_integration.marketplacepropertylisting')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_transactions', to='core.property')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('marketplace_user_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
    ]
