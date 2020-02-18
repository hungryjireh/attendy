# Generated by Django 2.1.5 on 2020-02-18 00:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0009_auto_20200218_0038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendanceformat',
            name='classroom',
        ),
        migrations.AddField(
            model_name='attendanceformat',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attendanceformat',
            name='name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
