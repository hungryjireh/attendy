# Generated by Django 2.1.5 on 2020-02-18 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_auto_20200218_0041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendanceformat',
            old_name='user',
            new_name='classroom',
        ),
    ]
