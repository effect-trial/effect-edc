# Generated by Django 3.2.11 on 2022-02-28 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edc_action_item', '0028_auto_20210203_0706'),
        ('effect_lists', '0005_delete_rankinscore'),
        ('effect_subject', '0022_auto_20220228_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalvitalsigns',
            name='crf_status',
        ),
        migrations.RemoveField(
            model_name='historicalvitalsigns',
            name='crf_status_comments',
        ),
        migrations.RemoveField(
            model_name='vitalsigns',
            name='crf_status',
        ),
        migrations.RemoveField(
            model_name='vitalsigns',
            name='crf_status_comments',
        ),
        migrations.AddField(
            model_name='historicalvitalsigns',
            name='action_identifier',
            field=models.CharField(db_index=True, default='0', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalvitalsigns',
            name='action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.actionitem'),
        ),
        migrations.AddField(
            model_name='historicalvitalsigns',
            name='action_item_reason',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='historicalvitalsigns',
            name='parent_action_identifier',
            field=models.CharField(blank=True, help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='historicalvitalsigns',
            name='parent_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.actionitem'),
        ),
        migrations.AddField(
            model_name='historicalvitalsigns',
            name='related_action_identifier',
            field=models.CharField(blank=True, help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='historicalvitalsigns',
            name='related_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.actionitem'),
        ),
        migrations.AddField(
            model_name='historicalvitalsigns',
            name='tracking_identifier',
            field=models.CharField(db_index=True, default='0', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vitalsigns',
            name='action_identifier',
            field=models.CharField(default='0', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vitalsigns',
            name='action_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='edc_action_item.actionitem'),
        ),
        migrations.AddField(
            model_name='vitalsigns',
            name='action_item_reason',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='vitalsigns',
            name='parent_action_identifier',
            field=models.CharField(blank=True, help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='vitalsigns',
            name='parent_action_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='edc_action_item.actionitem'),
        ),
        migrations.AddField(
            model_name='vitalsigns',
            name='related_action_identifier',
            field=models.CharField(blank=True, help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='vitalsigns',
            name='related_action_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='edc_action_item.actionitem'),
        ),
        migrations.AddField(
            model_name='vitalsigns',
            name='tracking_identifier',
            field=models.CharField(default='0', max_length=32, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='diagnoses',
            name='patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been admitted due to any of these diagnoses?'),
        ),
        migrations.AlterField(
            model_name='diagnoses',
            name='reportable_as_ae',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Are any of these diagnoses Grade 3 or above?'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='hospitalized',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been hospitalized since the last assessment?'),
        ),
        migrations.AlterField(
            model_name='historicaldiagnoses',
            name='patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been admitted due to any of these diagnoses?'),
        ),
        migrations.AlterField(
            model_name='historicaldiagnoses',
            name='reportable_as_ae',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Are any of these diagnoses Grade 3 or above?'),
        ),
        migrations.AlterField(
            model_name='historicalfollowup',
            name='hospitalized',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been hospitalized since the last assessment?'),
        ),
        migrations.AlterField(
            model_name='historicalmentalstatus',
            name='ecog_score',
            field=models.CharField(choices=[('0', '[0] Fully active, able to carry on all pre-disease performance without restriction'), ('1', '[1] Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature, e.g., light house work, office work'), ('2', '[2] Ambulatory and capable of all self-care but unable to carry out any work activities; up and about more than 50% of waking hours '), ('3', '[3] Capable of only limited self-care; confined to bed or chair more than 50% of waking hours'), ('4', '[4] Completely disabled; cannot carry on any self-care; totally confined to bed or chair'), ('5', '[5] Deceased')], max_length=15, verbose_name='ECOG score?'),
        ),
        migrations.AlterField(
            model_name='historicalmentalstatus',
            name='patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been admitted due to these symptoms?'),
        ),
        migrations.AlterField(
            model_name='historicalmentalstatus',
            name='reportable_as_ae',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Are any of these symptoms Grade 3 or above?'),
        ),
        migrations.AlterField(
            model_name='historicalsignsandsymptoms',
            name='cm_sx_patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='If the patient has CM signs or symptoms, was the patient admitted?'),
        ),
        migrations.AlterField(
            model_name='historicalsignsandsymptoms',
            name='patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been admitted due to any of these signs or symptoms?'),
        ),
        migrations.AlterField(
            model_name='historicalsignsandsymptoms',
            name='reportable_as_ae',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Are any of these signs or symptoms Grade 3 or above?'),
        ),
        migrations.AlterField(
            model_name='historicalvitalsigns',
            name='patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been admitted due to any of the above?'),
        ),
        migrations.AlterField(
            model_name='historicalvitalsigns',
            name='reportable_as_ae',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Are any of the above reportable as Grade 3 or above?'),
        ),
        migrations.AlterField(
            model_name='mentalstatus',
            name='ecog_score',
            field=models.CharField(choices=[('0', '[0] Fully active, able to carry on all pre-disease performance without restriction'), ('1', '[1] Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature, e.g., light house work, office work'), ('2', '[2] Ambulatory and capable of all self-care but unable to carry out any work activities; up and about more than 50% of waking hours '), ('3', '[3] Capable of only limited self-care; confined to bed or chair more than 50% of waking hours'), ('4', '[4] Completely disabled; cannot carry on any self-care; totally confined to bed or chair'), ('5', '[5] Deceased')], max_length=15, verbose_name='ECOG score?'),
        ),
        migrations.AlterField(
            model_name='mentalstatus',
            name='patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been admitted due to these symptoms?'),
        ),
        migrations.AlterField(
            model_name='mentalstatus',
            name='reportable_as_ae',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Are any of these symptoms Grade 3 or above?'),
        ),
        migrations.AlterField(
            model_name='signsandsymptoms',
            name='cm_sx_patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='If the patient has CM signs or symptoms, was the patient admitted?'),
        ),
        migrations.AlterField(
            model_name='signsandsymptoms',
            name='current_sx_gte_g3',
            field=models.ManyToManyField(help_text='If yes, complete AE Initial report.</br>', related_name='sx_gte_g3', to='effect_lists.SiSx', verbose_name='For these signs/symptoms, were any Grade 3 or above?'),
        ),
        migrations.AlterField(
            model_name='signsandsymptoms',
            name='patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been admitted due to any of these signs or symptoms?'),
        ),
        migrations.AlterField(
            model_name='signsandsymptoms',
            name='reportable_as_ae',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Are any of these signs or symptoms Grade 3 or above?'),
        ),
        migrations.AlterField(
            model_name='vitalsigns',
            name='patient_admitted',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Has the patient been admitted due to any of the above?'),
        ),
        migrations.AlterField(
            model_name='vitalsigns',
            name='reportable_as_ae',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If yes, complete AE Initial report.', max_length=15, verbose_name='Are any of the above reportable as Grade 3 or above?'),
        ),
    ]
