# Generated by Django 4.2.6 on 2024-02-20 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wdmmorpg', '0003_alter_taskplayer_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskplayer',
            name='project',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='taskplayers', to='wdmmorpg.Project'),
        ),

        migrations.AlterField(
            model_name='taskplayer',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projectss', to='wdmmorpg.project'),
        ),
    ]
