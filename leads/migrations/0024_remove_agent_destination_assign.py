# Generated by Django 4.2.8 on 2024-01-01 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0023_agent_destination_assign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='destination_assign',
        ),
    ]
