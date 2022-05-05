# Generated by Django 3.2.8 on 2022-04-11 13:29

import edc_model.models.validators.date
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_screening", "0017_auto_20220405_1936"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="any_other_mg_ssx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="any other clinical symptoms/signs of symptomatic meningitis?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="breast_feeding",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient breastfeeding?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="consent_ability",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Does the patient have capacity to provide informed consent for participation?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="contraindicated_meds",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Refer to the protocol for a complete list",
                max_length=25,
                verbose_name="Is the patient taking any contraindicated concomitant medications?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="jaundice",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Based on clinical examination, does the patient have jaundice?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="lp_done",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If YES, provide date below",
                max_length=15,
                null=True,
                verbose_name="Was LP done?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="mg_gcs_lt_15",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="a Glasgow Coma Scale (GCS) score of <15?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="mg_headache_nuchal_rigidity",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="a headache and marked nuchal rigidity?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="mg_headache_vomiting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="a headache and vomiting?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="mg_seizures",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")], max_length=25, verbose_name="seizures?"
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="mg_severe_headache",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="a progressively severe headache?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="on_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Is the patient already taking high-dose fluconazole treatment (800-1200 mg/day) for ≥1 week?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="prior_cm_epidose",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Has the patient had a prior episode of CM?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="reaction_to_study_drugs",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Has the patient had any serious reaction to flucytosine or fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="serum_crag_date",
            field=models.DateField(
                help_text="Test must have been performed within the last 14 days",
                null=True,
                validators=[edc_model.models.validators.date.date_not_future],
                verbose_name="Date of serum/plasma CrAg result",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="serum_crag_value",
            field=models.CharField(
                choices=[("POS", "Positive"), ("NEG", "Negative")],
                max_length=15,
                verbose_name="Serum/plasma CrAg result",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="willing_to_participate",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Is the patient willing to participate in the study if found eligible?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="any_other_mg_ssx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="any other clinical symptoms/signs of symptomatic meningitis?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="breast_feeding",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient breastfeeding?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="consent_ability",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Does the patient have capacity to provide informed consent for participation?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="contraindicated_meds",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Refer to the protocol for a complete list",
                max_length=25,
                verbose_name="Is the patient taking any contraindicated concomitant medications?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="jaundice",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Based on clinical examination, does the patient have jaundice?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="lp_done",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If YES, provide date below",
                max_length=15,
                null=True,
                verbose_name="Was LP done?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="mg_gcs_lt_15",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="a Glasgow Coma Scale (GCS) score of <15?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="mg_headache_nuchal_rigidity",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="a headache and marked nuchal rigidity?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="mg_headache_vomiting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="a headache and vomiting?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="mg_seizures",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")], max_length=25, verbose_name="seizures?"
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="mg_severe_headache",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="a progressively severe headache?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="on_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Is the patient already taking high-dose fluconazole treatment (800-1200 mg/day) for ≥1 week?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="prior_cm_epidose",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Has the patient had a prior episode of CM?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="reaction_to_study_drugs",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Has the patient had any serious reaction to flucytosine or fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="serum_crag_date",
            field=models.DateField(
                help_text="Test must have been performed within the last 14 days",
                null=True,
                validators=[edc_model.models.validators.date.date_not_future],
                verbose_name="Date of serum/plasma CrAg result",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="serum_crag_value",
            field=models.CharField(
                choices=[("POS", "Positive"), ("NEG", "Negative")],
                max_length=15,
                verbose_name="Serum/plasma CrAg result",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="willing_to_participate",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Is the patient willing to participate in the study if found eligible?",
            ),
        ),
    ]
