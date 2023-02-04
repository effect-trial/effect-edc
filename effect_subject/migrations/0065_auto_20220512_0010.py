# Generated by Django 3.2.8 on 2022-05-11 22:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0064_auto_20220511_2105"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalpatienthistory",
            name="current_arv_decision",
        ),
        migrations.RemoveField(
            model_name="patienthistory",
            name="current_arv_decision",
        ),
        migrations.AddField(
            model_name="arvhistory",
            name="art_decision",
            field=models.CharField(
                choices=[
                    ("N/A", "Not applicable"),
                    ("art_continued", "ART continued"),
                    ("art_stopped", "ART stopped"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="What decision was made at enrolment regarding their <u>current</u> ART regimen?",
            ),
        ),
        migrations.AddField(
            model_name="historicalarvhistory",
            name="art_decision",
            field=models.CharField(
                choices=[
                    ("N/A", "Not applicable"),
                    ("art_continued", "ART continued"),
                    ("art_stopped", "ART stopped"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="What decision was made at enrolment regarding their <u>current</u> ART regimen?",
            ),
        ),
    ]
