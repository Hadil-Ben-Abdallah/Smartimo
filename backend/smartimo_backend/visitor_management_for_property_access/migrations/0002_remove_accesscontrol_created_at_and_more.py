# Generated by Django 5.0.7 on 2024-08-28 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_management_for_property_access', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesscontrol',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='accesscontrol',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='showing',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='showing',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='visitor',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='visitor',
            name='updated_at',
        ),
    ]
