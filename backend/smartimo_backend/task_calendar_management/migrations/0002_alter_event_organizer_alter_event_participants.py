# Generated by Django 5.0.7 on 2024-08-28 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_category_remove_feedback_created_at_and_more'),
        ('task_calendar_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_organized', to='core.user'),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='events_participated', to='core.user'),
        ),
    ]
