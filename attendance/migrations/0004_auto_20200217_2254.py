# Generated by Django 2.1.5 on 2020-02-17 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_nominalroll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nominalroll',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
