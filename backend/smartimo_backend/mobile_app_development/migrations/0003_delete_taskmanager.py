# Generated by Django 5.0.7 on 2024-08-12 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_app_development', '0002_remove_mobileuseraccount_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TaskManager',
        ),
    ]