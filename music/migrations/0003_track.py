# Generated by Django 4.2.6 on 2024-01-02 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_playlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
                ('album_art', models.ImageField(upload_to='album_art/')),
                ('audio_file', models.FileField(upload_to='tracks/')),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
    ]