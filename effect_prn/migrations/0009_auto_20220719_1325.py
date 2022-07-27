# Generated by Django 3.2.13 on 2022-07-19 11:25

from django.db import migrations, models
import edc_model.validators.date
import edc_protocol.validators


class Migration(migrations.Migration):

    dependencies = [
        ('effect_lists', '0010_auto_20220719_1325'),
        ('effect_prn', '0008_auto_20220712_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='endofstudy',
            name='consent_withdrawal_reason',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='If participant withdrew consent, please specify reason ...'),
        ),
        migrations.AddField(
            model_name='endofstudy',
            name='invalid_enrol_reason',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='If participant was included in error, please provide narrative ...'),
        ),
        migrations.AddField(
            model_name='endofstudy',
            name='late_exclusion_reasons',
            field=models.ManyToManyField(blank=True, help_text='Select all that apply.', to='effect_lists.LateExclusionCriteria', verbose_name='If fulfilled late exclusion criteria, please specify which ...'),
        ),
        migrations.AddField(
            model_name='historicalendofstudy',
            name='consent_withdrawal_reason',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='If participant withdrew consent, please specify reason ...'),
        ),
        migrations.AddField(
            model_name='historicalendofstudy',
            name='invalid_enrol_reason',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='If participant was included in error, please provide narrative ...'),
        ),
        migrations.AlterField(
            model_name='endofstudy',
            name='death_date',
            field=models.DateField(blank=True, null=True, validators=[edc_protocol.validators.date_not_before_study_start, edc_model.validators.date.date_not_future], verbose_name='If died, what was the date of death?'),
        ),
        migrations.AlterField(
            model_name='endofstudy',
            name='ltfu_date',
            field=models.DateField(blank=True, null=True, validators=[edc_protocol.validators.date_not_before_study_start, edc_model.validators.date.date_not_future], verbose_name='If lost to follow-up, on what date?'),
        ),
        migrations.AlterField(
            model_name='endofstudy',
            name='other_offschedule_reason',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='If OTHER, please specify reason ...'),
        ),
        migrations.AlterField(
            model_name='endofstudy',
            name='transferred_consent',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=15, verbose_name='If transferred, has the participant provided consent to be followed-up for 6 month end-point?'),
        ),
        migrations.AlterField(
            model_name='historicalendofstudy',
            name='death_date',
            field=models.DateField(blank=True, null=True, validators=[edc_protocol.validators.date_not_before_study_start, edc_model.validators.date.date_not_future], verbose_name='If died, what was the date of death?'),
        ),
        migrations.AlterField(
            model_name='historicalendofstudy',
            name='ltfu_date',
            field=models.DateField(blank=True, null=True, validators=[edc_protocol.validators.date_not_before_study_start, edc_model.validators.date.date_not_future], verbose_name='If lost to follow-up, on what date?'),
        ),
        migrations.AlterField(
            model_name='historicalendofstudy',
            name='other_offschedule_reason',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='If OTHER, please specify reason ...'),
        ),
        migrations.AlterField(
            model_name='historicalendofstudy',
            name='transferred_consent',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', max_length=15, verbose_name='If transferred, has the participant provided consent to be followed-up for 6 month end-point?'),
        ),
    ]