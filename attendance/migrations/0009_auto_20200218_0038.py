# Generated by Django 2.1.5 on 2020-02-18 00:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_auto_20200218_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceformat',
            name='classroom',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendanceformat',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to=settings.AUTH_USER_MODEL),
        ),
    ]
