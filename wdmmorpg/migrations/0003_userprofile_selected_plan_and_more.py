# Generated by Django 5.0 on 2023-12-21 13:53

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_selection', '0001_initial'),
        ('wdmmorpg', '0002_remove_project_priority_consumable_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='selected_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='plan_selection.plan'),
        ),
        migrations.AlterField(
            model_name='usertaskinteraction',
            name='end_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 12, 31, 23, 59, 59), null=True),
        ),
    ]