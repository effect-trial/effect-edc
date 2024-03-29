# Generated by Django 4.1.7 on 2023-08-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_lists", "0013_auto_20220927_1831"),
        ("effect_subject", "0107_alter_diagnoses_diagnoses_other_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diagnoses",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been NEWLY admitted due to any of the above?",
            ),
        ),
        migrations.AlterField(
            model_name="diagnoses",
            name="reportable_as_ae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is NEWLY reportable (or present at baseline).<br/>If YES (and not baseline), complete AE Initial report.",
                max_length=15,
                verbose_name="Are any of the above Grade 3 or above, and NEWLY reportable?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnoses",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been NEWLY admitted due to any of the above?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnoses",
            name="reportable_as_ae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is NEWLY reportable (or present at baseline).<br/>If YES (and not baseline), complete AE Initial report.",
                max_length=15,
                verbose_name="Are any of the above Grade 3 or above, and NEWLY reportable?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmentalstatus",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been NEWLY admitted due to any of the above?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmentalstatus",
            name="reportable_as_ae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is NEWLY reportable (or present at baseline).<br/>If YES (and not baseline), complete AE Initial report.",
                max_length=15,
                verbose_name="Are any of the above Grade 3 or above, and NEWLY reportable?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsignsandsymptoms",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been NEWLY admitted due to any of the above?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsignsandsymptoms",
            name="reportable_as_ae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is NEWLY reportable (or present at baseline).<br/>If YES (and not baseline), complete AE Initial report.",
                max_length=15,
                verbose_name="Are any of the above Grade 3 or above, and NEWLY reportable?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="hospitalized",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable (if missed)"),
                ],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been hospitalized since the last assessment?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalvitalsigns",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been NEWLY admitted due to any of the above?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalvitalsigns",
            name="reportable_as_ae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is NEWLY reportable (or present at baseline).<br/>If YES (and not baseline), complete AE Initial report.",
                max_length=15,
                verbose_name="Are any of the above Grade 3 or above, and NEWLY reportable?",
            ),
        ),
        migrations.AlterField(
            model_name="mentalstatus",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been NEWLY admitted due to any of the above?",
            ),
        ),
        migrations.AlterField(
            model_name="mentalstatus",
            name="reportable_as_ae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is NEWLY reportable (or present at baseline).<br/>If YES (and not baseline), complete AE Initial report.",
                max_length=15,
                verbose_name="Are any of the above Grade 3 or above, and NEWLY reportable?",
            ),
        ),
        migrations.AlterField(
            model_name="signsandsymptoms",
            name="current_sx_gte_g3",
            field=models.ManyToManyField(
                help_text="Only answer YES if this is NEWLY reportable (or present at baseline).<br/>If YES (and not baseline), complete AE Initial report.</br>",
                related_name="sx_gte_g3",
                to="effect_lists.sisx",
                verbose_name="For these signs/symptoms, were any Grade 3 or above?",
            ),
        ),
        migrations.AlterField(
            model_name="signsandsymptoms",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been NEWLY admitted due to any of the above?",
            ),
        ),
        migrations.AlterField(
            model_name="signsandsymptoms",
            name="reportable_as_ae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is NEWLY reportable (or present at baseline).<br/>If YES (and not baseline), complete AE Initial report.",
                max_length=15,
                verbose_name="Are any of the above Grade 3 or above, and NEWLY reportable?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="hospitalized",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable (if missed)"),
                ],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been hospitalized since the last assessment?",
            ),
        ),
        migrations.AlterField(
            model_name="vitalsigns",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is a NEW admission (or already admitted at baseline).<br/>If YES (and not baseline), complete Hospitalization and AE Initial reports.",
                max_length=15,
                verbose_name="Has the participant been NEWLY admitted due to any of the above?",
            ),
        ),
        migrations.AlterField(
            model_name="vitalsigns",
            name="reportable_as_ae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Only answer YES if this is NEWLY reportable (or present at baseline).<br/>If YES (and not baseline), complete AE Initial report.",
                max_length=15,
                verbose_name="Are any of the above Grade 3 or above, and NEWLY reportable?",
            ),
        ),
    ]
