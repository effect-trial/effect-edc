# Generated by Django 4.2.10 on 2024-02-23 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_consent", "0013_alter_historicalsubjectconsent_site_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="subjectconsent",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="historicalsubjectconsent",
            name="hcw_data_sharing",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Does the ppt agree to sharing study information with their primary healthcare provider? ",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectconsent",
            name="he_substudy",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Does the ppt agree to participate in the Health Economics sub-study?",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectconsent",
            name="sample_export",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Does the ppt agree to export of stored samples internationally?",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectconsent",
            name="sample_storage",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Does the ppt agree to storage of samples in-country?",
            ),
        ),
        migrations.AddField(
            model_name="subjectconsent",
            name="hcw_data_sharing",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Does the ppt agree to sharing study information with their primary healthcare provider? ",
            ),
        ),
        migrations.AddField(
            model_name="subjectconsent",
            name="he_substudy",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Does the ppt agree to participate in the Health Economics sub-study?",
            ),
        ),
        migrations.AddField(
            model_name="subjectconsent",
            name="sample_export",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Does the ppt agree to export of stored samples internationally?",
            ),
        ),
        migrations.AddField(
            model_name="subjectconsent",
            name="sample_storage",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Does the ppt agree to storage of samples in-country?",
            ),
        ),
    ]
