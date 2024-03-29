# Generated by Django 4.2.8 on 2023-12-31 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('destination', '0001_initial'),
        ('leads', '0015_followup_date_added_lead_converted_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='destination_assign',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='destination.destination'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_organisor',
            field=models.BooleanField(default=False),
        ),
    ]
