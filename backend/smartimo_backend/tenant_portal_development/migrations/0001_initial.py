# Generated by Django 5.0.7 on 2024-08-12 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_user_password'),
        ('lease_rental_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portal_name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=50)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='TenantNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notification')),
                ('type', models.CharField(max_length=255)),
                ('delivery_method', models.CharField(max_length=50)),
                ('frequency', models.CharField(max_length=50)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lease_rental_management.tenant')),
            ],
            bases=('core.notification',),
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
