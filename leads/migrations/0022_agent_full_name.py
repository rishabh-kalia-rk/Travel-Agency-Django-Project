# Generated by Django 4.2.8 on 2024-01-01 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0021_alter_lead_destination'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='full_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]