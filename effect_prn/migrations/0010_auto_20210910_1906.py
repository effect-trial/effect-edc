# Generated by Django 3.2.6 on 2021-09-10 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_protocol_violation", "0001_initial"),
        ("meta_prn", "0009_auto_20210910_0239"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalprotocoldeviationviolation",
            old_name="action_required",
            new_name="action_required_old",
        ),
        migrations.RenameField(
            model_name="protocoldeviationviolation",
            old_name="action_required",
            new_name="action_required_old",
        ),
        migrations.AlterField(
            model_name="historicalprotocoldeviationviolation",
            name="action_required_old",
            field=models.CharField(
                choices=[
                    ("remain_on_study", "Participant to remain on trial"),
                    ("to_be_withdrawn", "Participant to be withdrawn from trial"),
                    (
                        "remain_on_study_modified",
                        "Patient remains on study but data analysis will be modified",
                    ),
                ],
                max_length=45,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="protocoldeviationviolation",
            name="action_required_old",
            field=models.CharField(
                choices=[
                    ("remain_on_study", "Participant to remain on trial"),
                    ("to_be_withdrawn", "Participant to be withdrawn from trial"),
                    (
                        "remain_on_study_modified",
                        "Patient remains on study but data analysis will be modified",
                    ),
                ],
                max_length=45,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalprotocoldeviationviolation",
            name="action_required",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_protocol_violation.actionsrequired",
            ),
        ),
        migrations.AddField(
            model_name="protocoldeviationviolation",
            name="action_required",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="edc_protocol_violation.actionsrequired",
            ),
        ),
    ]
