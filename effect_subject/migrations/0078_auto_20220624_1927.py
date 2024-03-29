# Generated by Django 3.2.13 on 2022-06-24 17:27

from django.db import migrations, models
import edc_model.models.fields.date_estimated
import edc_model.validators.date


class Migration(migrations.Migration):
    dependencies = [
        ("effect_lists", "0009_delete_bloodtests"),
        ("effect_subject", "0077_auto_20220624_1230"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalpatienthistory",
            name="on_rifampicin",
        ),
        migrations.RemoveField(
            model_name="historicalpatienthistory",
            name="rifampicin_start_date",
        ),
        migrations.RemoveField(
            model_name="historicalpatienthistory",
            name="tb_dx_ago",
        ),
        migrations.RemoveField(
            model_name="patienthistory",
            name="on_rifampicin",
        ),
        migrations.RemoveField(
            model_name="patienthistory",
            name="rifampicin_start_date",
        ),
        migrations.RemoveField(
            model_name="patienthistory",
            name="tb_dx_ago",
        ),
        migrations.AddField(
            model_name="historicalpatienthistory",
            name="tb_dx_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If YES, give date",
            ),
        ),
        migrations.AddField(
            model_name="historicalpatienthistory",
            name="tb_dx_date_estimated",
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
            model_name="historicalpatienthistory",
            name="tb_tx_type",
            field=models.CharField(
                choices=[
                    ("active_tb", "Active TB"),
                    ("latent_tb", "Latent TB (HR: Isoniazid + Rifampicin)"),
                    ("ipt", "IPT (Isoniazid Preventive Therapy)"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="If 'Active TB' please specify treatment below ...",
                max_length=15,
                verbose_name="If YES, please specify type?",
            ),
        ),
        migrations.AddField(
            model_name="patienthistory",
            name="active_tb_tx",
            field=models.ManyToManyField(
                blank=True,
                to="effect_lists.TbTreatments",
                verbose_name="If 'Active TB', which treatment?",
            ),
        ),
        migrations.AddField(
            model_name="patienthistory",
            name="tb_dx_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If YES, give date",
            ),
        ),
        migrations.AddField(
            model_name="patienthistory",
            name="tb_dx_date_estimated",
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
            model_name="patienthistory",
            name="tb_tx_type",
            field=models.CharField(
                choices=[
                    ("active_tb", "Active TB"),
                    ("latent_tb", "Latent TB (HR: Isoniazid + Rifampicin)"),
                    ("ipt", "IPT (Isoniazid Preventive Therapy)"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="If 'Active TB' please specify treatment below ...",
                max_length=15,
                verbose_name="If YES, please specify type?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="on_tb_tx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                verbose_name="Are you currently taking TB treatment?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="on_tb_tx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                verbose_name="Are you currently taking TB treatment?",
            ),
        ),
    ]
