# Generated by Django 2.1.5 on 2020-02-18 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_auto_20200217_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='nominalroll',
            name='saved_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]