# Generated by Django 5.1.3 on 2025-02-01 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='is_approved',
        ),
    ]
