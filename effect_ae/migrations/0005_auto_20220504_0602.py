# Generated by Django 3.2.11 on 2022-05-04 03:02

import edc_model.models.fields.date_estimated
import edc_model.validators.date
import edc_protocol.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_ae", "0004_auto_20220419_2126"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deathreport",
            name="death_certificate",
        ),
        migrations.RemoveField(
            model_name="deathreport",
            name="death_location_name",
        ),
        migrations.RemoveField(
            model_name="deathreport",
            name="death_location_type",
        ),
        migrations.RemoveField(
            model_name="deathreport",
            name="informant_contacts",
        ),
        migrations.RemoveField(
            model_name="deathreport",
            name="informant_relationship",
        ),
        migrations.RemoveField(
            model_name="deathreport",
            name="other_informant_relationship",
        ),
        migrations.RemoveField(
            model_name="deathreport",
            name="secondary_cause_of_death",
        ),
        migrations.RemoveField(
            model_name="deathreport",
            name="secondary_cause_of_death_other",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreport",
            name="death_certificate",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreport",
            name="death_location_name",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreport",
            name="death_location_type",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreport",
            name="informant_contacts",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreport",
            name="informant_relationship",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreport",
            name="other_informant_relationship",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreport",
            name="secondary_cause_of_death",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreport",
            name="secondary_cause_of_death_other",
        ),
        migrations.AddField(
            model_name="deathreport",
            name="date_first_unwell",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[
                    edc_model.validators.date.date_not_future,
                    edc_protocol.validators.date_not_before_study_start,
                ],
                verbose_name="If YES, when did they first become unwell?",
            ),
        ),
        migrations.AddField(
            model_name="deathreport",
            name="date_first_unwell_estimated",
            field=edc_model.models.fields.date_estimated.IsDateEstimatedFieldNa(
                choices=[
                    ("N/A", "Not applicable"),
                    ("not_estimated", "No."),
                    ("D", "Yes, estimated the Day"),
                    ("MD", "Yes, estimated Month and Day"),
                    ("YMD", "Yes, estimated Year, Month and Day"),
                ],
                default="N/A",
                help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                max_length=25,
                verbose_name="If YES, is this date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="deathreport",
            name="drowsy_confused_altered_behaviour",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, did they become drowsy, confused of have altered behaviour?",
            ),
        ),
        migrations.AddField(
            model_name="deathreport",
            name="headache",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, did they complain of a headache during this illness?",
            ),
        ),
        migrations.AddField(
            model_name="deathreport",
            name="nok_narrative",
            field=models.TextField(
                blank=True, null=True, verbose_name="Next of kin narrative"
            ),
        ),
        migrations.AddField(
            model_name="deathreport",
            name="seizures",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, did they have any seizures?",
            ),
        ),
        migrations.AddField(
            model_name="deathreport",
            name="speak_nok",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                help_text="If YES, include other details of conversation in 'Next of kin narrative'",
                max_length=5,
                verbose_name="Did study staff speak to NOK following death?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="date_first_unwell",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[
                    edc_model.validators.date.date_not_future,
                    edc_protocol.validators.date_not_before_study_start,
                ],
                verbose_name="If YES, when did they first become unwell?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="date_first_unwell_estimated",
            field=edc_model.models.fields.date_estimated.IsDateEstimatedFieldNa(
                choices=[
                    ("N/A", "Not applicable"),
                    ("not_estimated", "No."),
                    ("D", "Yes, estimated the Day"),
                    ("MD", "Yes, estimated Month and Day"),
                    ("YMD", "Yes, estimated Year, Month and Day"),
                ],
                default="N/A",
                help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                max_length=25,
                verbose_name="If YES, is this date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="drowsy_confused_altered_behaviour",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, did they become drowsy, confused of have altered behaviour?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="headache",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, did they complain of a headache during this illness?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="nok_narrative",
            field=models.TextField(
                blank=True, null=True, verbose_name="Next of kin narrative"
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="seizures",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, did they have any seizures?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="speak_nok",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                help_text="If YES, include other details of conversation in 'Next of kin narrative'",
                max_length=5,
                verbose_name="Did study staff speak to NOK following death?",
            ),
            preserve_default=False,
        ),
    ]
