# Generated by Django 2.0.2 on 2018-06-02 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_zsuser_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zsuser',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnail', verbose_name='Thumbnail'),
        ),
    ]
