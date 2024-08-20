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
            name='TenantNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notification')),
                ('type', models.CharField(choices=[('lease_renewal', 'Lease Renewal'), ('rent_increase', 'Rent Increase')], default='lease_renewal', max_length=255)),
                ('delivery_method', models.CharField(choices=[('email', 'Email'), ('sms', 'SMS')], default='email', max_length=50)),
                ('frequency', models.CharField(max_length=50)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lease_rental_management.tenant')),
            ],
            bases=('core.notification',),
        ),
        migrations.CreateModel(
            name='TenantPortal',
            fields=[
                ('portal_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.portal')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lease_rental_management.tenant')),
            ],
            bases=('core.portal',),
        ),
        migrations.CreateModel(
            name='TenantResource',
            fields=[
                ('resource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.resource')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lease_rental_management.tenant')),
            ],
            bases=('core.resource',),
        ),
    ]
