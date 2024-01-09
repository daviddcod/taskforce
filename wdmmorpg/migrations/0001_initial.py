# Generated by Django 4.2.6 on 2024-01-08 14:54

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plan_selection', '0002_plan_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('material', models.CharField(max_length=100)),
                ('effect', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PriorityScale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('missions', models.ManyToManyField(to='wdmmorpg.mission')),
                ('priority', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='wdmmorpg.priorityscale')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('experience_gained', models.IntegerField(default=0)),
                ('completed_on', models.DateTimeField(blank=True, null=True)),
                ('environment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wdmmorpg.environment')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wdmmorpg.priorityscale')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('experience', models.IntegerField(default=0)),
                ('prestige', models.IntegerField(default=0)),
                ('health', models.IntegerField(default=100)),
                ('endurance', models.IntegerField(default=100)),
                ('mind', models.IntegerField(default=100)),
                ('selected_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='plan_selection.plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTaskInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, default=datetime.datetime(2024, 12, 31, 23, 59, 59), null=True)),
                ('achievements', models.JSONField(default=dict)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wdmmorpg.task')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='usertaskinteractions', to='wdmmorpg.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TransportationKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('type', models.CharField(default='public', max_length=100)),
                ('access_level', models.CharField(default='Standard', max_length=100)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transportation_keys', to='wdmmorpg.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('quality', models.CharField(default='Standard', max_length=100)),
                ('type', models.CharField(default='digital', max_length=100)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tools', to='wdmmorpg.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TaskPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, default=datetime.datetime(2024, 12, 31, 23, 59, 59), null=True)),
                ('achievements', models.JSONField(default=dict)),
                ('current_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_task', to='wdmmorpg.task')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskplayers', to='wdmmorpg.project')),
                ('tasks', models.ManyToManyField(to='wdmmorpg.task')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_taskplayers', to='wdmmorpg.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='wdmmorpg.userprofile'),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('level', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wdmmorpg.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('points', models.IntegerField()),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ranks', to='wdmmorpg.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='wdmmorpg.userprofile'),
        ),
        migrations.AddField(
            model_name='priorityscale',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wdmmorpg.rank'),
        ),
        migrations.AddField(
            model_name='priorityscale',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='priority_scales', to='wdmmorpg.userprofile'),
        ),
        migrations.AddField(
            model_name='mission',
            name='priority',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wdmmorpg.priorityscale'),
        ),
        migrations.AddField(
            model_name='mission',
            name='tasks',
            field=models.ManyToManyField(to='wdmmorpg.task'),
        ),
        migrations.AddField(
            model_name='mission',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='missions', to='wdmmorpg.userprofile'),
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('item_type', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wdmmorpg.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumables', models.ManyToManyField(blank=True, to='wdmmorpg.consumable')),
                ('tools', models.ManyToManyField(blank=True, to='wdmmorpg.tool')),
                ('transportation_keys', models.ManyToManyField(blank=True, to='wdmmorpg.transportationkey')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to='wdmmorpg.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='environment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='environments', to='wdmmorpg.userprofile'),
        ),
        migrations.AddField(
            model_name='environment',
            name='users',
            field=models.ManyToManyField(to='wdmmorpg.userprofile'),
        ),
        migrations.AddField(
            model_name='consumable',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='consumables', to='wdmmorpg.userprofile'),
        ),
    ]
