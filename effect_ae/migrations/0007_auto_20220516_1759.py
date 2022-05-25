# Generated by Django 3.2.8 on 2022-05-16 15:59

from django.db import migrations, models
import edc_model.models.fields.date_estimated
import edc_model.models.validators.date
import edc_protocol.validators


class Migration(migrations.Migration):

    dependencies = [
        ('effect_ae', '0006_auto_20220516_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='deathreport',
            name='clinical_notes_available',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text='If YES, include details of admission in narrative', max_length=15, verbose_name='If YES, are clinical notes available to study staff?'),
        ),
        migrations.AddField(
            model_name='deathreport',
            name='cm_sx',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=15, verbose_name='If YES, do notes document any symptoms or signs of cryptococcal meningitis prior to death?'),
        ),
        migrations.AddField(
            model_name='deathreport',
            name='hospitalization_date',
            field=models.DateField(blank=True, null=True, validators=[edc_model.models.validators.date.date_not_future, edc_protocol.validators.date_not_before_study_start], verbose_name='If YES, date of hospitalisation'),
        ),
        migrations.AddField(
            model_name='deathreport',
            name='hospitalization_date_estimated',
            field=edc_model.models.fields.date_estimated.IsDateEstimatedFieldNa(choices=[('N/A', 'Not applicable'), ('not_estimated', 'No.'), ('D', 'Yes, estimated the Day'), ('MD', 'Yes, estimated Month and Day'), ('YMD', 'Yes, estimated Year, Month and Day')], default='N/A', help_text='If the exact date is not known, please indicate which part of the date is estimated.', max_length=25, verbose_name='If YES, is this date estimated?'),
        ),
        migrations.AddField(
            model_name='historicaldeathreport',
            name='clinical_notes_available',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text='If YES, include details of admission in narrative', max_length=15, verbose_name='If YES, are clinical notes available to study staff?'),
        ),
        migrations.AddField(
            model_name='historicaldeathreport',
            name='cm_sx',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=15, verbose_name='If YES, do notes document any symptoms or signs of cryptococcal meningitis prior to death?'),
        ),
        migrations.AddField(
            model_name='historicaldeathreport',
            name='hospitalization_date',
            field=models.DateField(blank=True, null=True, validators=[edc_model.models.validators.date.date_not_future, edc_protocol.validators.date_not_before_study_start], verbose_name='If YES, date of hospitalisation'),
        ),
        migrations.AddField(
            model_name='historicaldeathreport',
            name='hospitalization_date_estimated',
            field=edc_model.models.fields.date_estimated.IsDateEstimatedFieldNa(choices=[('N/A', 'Not applicable'), ('not_estimated', 'No.'), ('D', 'Yes, estimated the Day'), ('MD', 'Yes, estimated Month and Day'), ('YMD', 'Yes, estimated Year, Month and Day')], default='N/A', help_text='If the exact date is not known, please indicate which part of the date is estimated.', max_length=25, verbose_name='If YES, is this date estimated?'),
        ),
    ]