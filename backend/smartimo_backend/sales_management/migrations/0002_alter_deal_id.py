# Generated by Django 5.0.7 on 2024-08-07 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
