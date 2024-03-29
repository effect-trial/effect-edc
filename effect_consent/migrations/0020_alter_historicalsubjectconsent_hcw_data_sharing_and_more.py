# Generated by Django 4.2.11 on 2024-03-25 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_consent", "0019_update_consent_instance_model_names"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="hcw_data_sharing",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to sharing study information with their primary healthcare provider?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="he_substudy",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to participate in the Health Economics sub-study?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="sample_export",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                help_text="Select `Not applicable` if participant does not agree to store samples in-country.",
                max_length=15,
                verbose_name="Does the participant agree to export of stored samples internationally?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="sample_storage",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to storage of samples in-country?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentupdatev2",
            name="hcw_data_sharing",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to sharing study information with their primary healthcare provider?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentupdatev2",
            name="he_substudy",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to participate in the Health Economics sub-study?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentupdatev2",
            name="sample_export",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                help_text="Select `Not applicable` if participant does not agree to store samples in-country.",
                max_length=15,
                verbose_name="Does the participant agree to export of stored samples internationally?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentupdatev2",
            name="sample_storage",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to storage of samples in-country?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv1",
            name="hcw_data_sharing",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to sharing study information with their primary healthcare provider?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv1",
            name="he_substudy",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to participate in the Health Economics sub-study?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv1",
            name="sample_export",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                help_text="Select `Not applicable` if participant does not agree to store samples in-country.",
                max_length=15,
                verbose_name="Does the participant agree to export of stored samples internationally?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv1",
            name="sample_storage",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to storage of samples in-country?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv2",
            name="hcw_data_sharing",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to sharing study information with their primary healthcare provider?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv2",
            name="he_substudy",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to participate in the Health Economics sub-study?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv2",
            name="sample_export",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                help_text="Select `Not applicable` if participant does not agree to store samples in-country.",
                max_length=15,
                verbose_name="Does the participant agree to export of stored samples internationally?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv2",
            name="sample_storage",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to storage of samples in-country?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="hcw_data_sharing",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to sharing study information with their primary healthcare provider?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="he_substudy",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to participate in the Health Economics sub-study?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="sample_export",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                help_text="Select `Not applicable` if participant does not agree to store samples in-country.",
                max_length=15,
                verbose_name="Does the participant agree to export of stored samples internationally?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="sample_storage",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to storage of samples in-country?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsentupdatev2",
            name="hcw_data_sharing",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to sharing study information with their primary healthcare provider?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsentupdatev2",
            name="he_substudy",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to participate in the Health Economics sub-study?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsentupdatev2",
            name="sample_export",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                help_text="Select `Not applicable` if participant does not agree to store samples in-country.",
                max_length=15,
                verbose_name="Does the participant agree to export of stored samples internationally?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsentupdatev2",
            name="sample_storage",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Does the participant agree to storage of samples in-country?",
            ),
        ),
    ]
