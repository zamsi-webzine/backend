# Generated by Django 2.0.2 on 2018-06-02 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20180525_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('R', 're-view'), ('E', 'enter-view'), ('O', 'over-view')], default='R', max_length=1),
        ),
    ]