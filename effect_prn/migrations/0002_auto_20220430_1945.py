# Generated by Django 3.2.11 on 2022-04-30 16:45

from django.db import migrations
import edc_action_item.models.action_model_mixin


class Migration(migrations.Migration):

    dependencies = [
        ('effect_prn', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='losstofollowup',
            managers=[
                ('objects', edc_action_item.models.action_model_mixin.ActionItemModelManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='protocoldeviationviolation',
            managers=[
                ('objects', edc_action_item.models.action_model_mixin.ActionItemModelManager()),
            ],
        ),
    ]
