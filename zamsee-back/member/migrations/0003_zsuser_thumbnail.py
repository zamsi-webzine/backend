# Generated by Django 2.0.2 on 2018-05-19 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20180309_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='zsuser',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='thumbnail', verbose_name='Thumbnail'),
        ),
    ]
