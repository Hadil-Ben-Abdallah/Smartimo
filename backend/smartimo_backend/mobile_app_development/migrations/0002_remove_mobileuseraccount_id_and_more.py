# Generated by Django 5.0.7 on 2024-08-11 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_password'),
        ('mobile_app_development', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobileuseraccount',
            name='id',
        ),
        migrations.AddField(
            model_name='mobileuseraccount',
            name='user_ptr',
            field=models.OneToOneField(auto_created=True, default='', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.user'),
            preserve_default=False,
        ),
    ]