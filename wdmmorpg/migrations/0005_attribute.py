# Generated by Django 4.2.6 on 2024-02-29 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wdmmorpg', '0004_alter_taskplayer_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('total_points', models.IntegerField(default=100)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='attribute_user', to='wdmmorpg.userprofile')),
            ],
        ),
    ]
