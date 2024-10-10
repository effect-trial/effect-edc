# Generated by Django 4.2.11 on 2024-05-18 08:37

from django.db import migrations, models
import edc_model.validators.date


class Migration(migrations.Migration):

    dependencies = [
        (
            "effect_screening",
            "0046_historicalsubjectscreening_parent_guardian_consent_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="lp_date",
            field=models.DateField(
                blank=True,
                help_text="LP should be done AFTER serum/plasma CrAg, but may be done no more than 3 days before the serum/plasma CrAg.",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="LP date",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="preg_test_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Pregnancy test date (Urine or serum βhCG)",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="lp_date",
            field=models.DateField(
                blank=True,
                help_text="LP should be done AFTER serum/plasma CrAg, but may be done no more than 3 days before the serum/plasma CrAg.",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="LP date",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="preg_test_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Pregnancy test date (Urine or serum βhCG)",
            ),
        ),
    ]