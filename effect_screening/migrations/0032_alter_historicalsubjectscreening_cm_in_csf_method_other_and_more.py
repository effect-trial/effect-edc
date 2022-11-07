# Generated by Django 4.1.2 on 2022-11-07 11:54

from django.db import migrations
import edc_model_fields.fields.other_charfield


class Migration(migrations.Migration):

    dependencies = [
        ("effect_screening", "0031_alter_historicalsubjectscreening_csf_crag_value_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="cm_in_csf_method_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="cm_in_csf_method_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
    ]
