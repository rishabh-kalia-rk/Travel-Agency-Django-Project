# Generated by Django 4.2.8 on 2023-12-29 19:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0014_alter_lead_profile_picture_followup'),
    ]

    operations = [
        migrations.AddField(
            model_name='followup',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='converted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
