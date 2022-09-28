# Generated by Django 3.2 on 2022-09-27 16:31

from django.db import migrations, models
import edc_crf.model_mixins.crf_status_model_mixin


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0091_auto_20220920_1659"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="arvhistory",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "ARV History",
                "verbose_name_plural": "ARV History",
            },
        ),
        migrations.AlterModelOptions(
            name="patienthistory",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Patient History",
                "verbose_name_plural": "Patient History",
            },
        ),
        migrations.AlterField(
            model_name="adherence",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="arvhistory",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="arvtreatment",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="bloodculture",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="chestxray",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="clinicalnote",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="diagnoses",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomics",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicsevent",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="histopathology",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherence",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagefour",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestageone",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagethree",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagetwo",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalarvhistory",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalarvtreatment",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodculture",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalchestxray",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalnote",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnoses",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomics",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsevent",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhistopathology",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicallpcsf",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmedicationadherence",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmentalstatus",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienttreatment",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedication",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedicationbaseline",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedicationfollowup",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaltbdiagnostics",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="lpcsf",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="medicationadherence",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="mentalstatus",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="patienttreatment",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="studymedication",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AlterField(
            model_name="tbdiagnostics",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AddIndex(
            model_name="adherence",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_6dadf1_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="arvhistory",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_ff8288_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="arvtreatment",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_6e1579_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="bloodculture",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_86a4e2_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultschem",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_2c3966_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="bloodresultsfbc",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_110935_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="chestxray",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_761cb5_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="clinicalnote",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_412871_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="diagnoses",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_358e1d_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="healtheconomics",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_9a1364_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="healtheconomicsevent",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_65cbf3_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="histopathology",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_d3b7bf_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="lpcsf",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_e88b05_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="medicationadherence",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_4933e1_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="mentalstatus",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_aaccd7_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="patienthistory",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_207dfa_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="patienttreatment",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_4748cd_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="signsandsymptoms",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_d4739d_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="studymedication",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_079a9b_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="subjectrequisition",
            index=models.Index(
                fields=["subject_visit", "site", "panel", "id"],
                name="effect_subj_subject_401c00_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="subjectrequisition",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_2a3a05_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="subjectvisitmissed",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_25fa79_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="tbdiagnostics",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_211f20_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="urinalysis",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_20cb87_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="vitalsigns",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_a1c8af_idx",
            ),
        ),
    ]
