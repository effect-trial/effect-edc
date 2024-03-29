# Generated by Django 3.2 on 2022-09-29 10:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_lists", "0013_auto_20220927_1831"),
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("effect_subject", "0092_auto_20220927_1831"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HistoricalPatientHistory",
            new_name="HistoricalParticipantHistory",
        ),
        migrations.RenameModel(
            old_name="PatientHistory",
            new_name="ParticipantHistory",
        ),
        migrations.AlterModelOptions(
            name="historicalparticipanthistory",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Participant History",
                "verbose_name_plural": "historical Participant History",
            },
        ),
        migrations.AlterModelOptions(
            name="participanthistory",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Participant History",
                "verbose_name_plural": "Participant History",
            },
        ),
        migrations.RemoveIndex(
            model_name="participanthistory",
            name="effect_subj_subject_bb6b06_idx",
        ),
        migrations.RemoveIndex(
            model_name="participanthistory",
            name="effect_subj_subject_207dfa_idx",
        ),
        migrations.AddIndex(
            model_name="participanthistory",
            index=models.Index(
                fields=["subject_visit", "site", "id"], name="effect_subj_subject_9e5f19_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="participanthistory",
            index=models.Index(
                fields=["subject_visit", "report_datetime"],
                name="effect_subj_subject_e102c5_idx",
            ),
        ),
    ]
