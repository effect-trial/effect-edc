# Generated by Django 4.2.11 on 2024-06-26 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Rm792KwInCurrentSxGteG3Other",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("report_model", models.CharField(max_length=50)),
                ("subject_identifier", models.CharField(max_length=25)),
                ("created", models.DateTimeField()),
                ("visit_code", models.CharField(max_length=25)),
                ("visit_code_sequence", models.IntegerField(default=0)),
                ("current_sx_gte_g3_other", models.TextField()),
                ("user_created", models.CharField(max_length=25)),
                ("user_modified", models.CharField(max_length=25)),
                ("modified", models.DateTimeField()),
            ],
            options={
                "verbose_name": "Redmine #792.2: Signs and Symptoms: Keyword in other G3 sx",
                "verbose_name_plural": "Redmine #792.2: Signs and Symptoms: Keyword in other G3 sx",
                "db_table": "rm792_kw_in_current_sx_gte_g3_other",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Rm792KwInCurrentSxOther",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("report_model", models.CharField(max_length=50)),
                ("subject_identifier", models.CharField(max_length=25)),
                ("created", models.DateTimeField()),
                ("visit_code", models.CharField(max_length=25)),
                ("visit_code_sequence", models.IntegerField(default=0)),
                ("current_sx_other", models.TextField()),
                ("user_created", models.CharField(max_length=25)),
                ("user_modified", models.CharField(max_length=25)),
                ("modified", models.DateTimeField()),
            ],
            options={
                "verbose_name": "Redmine #792.1: Signs and Symptoms: Keyword in other sx",
                "verbose_name_plural": "Redmine #792.1: Signs and Symptoms: Keyword in other sx",
                "db_table": "rm792_kw_in_current_sx_other",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Rm792SiSxListCandidates",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("report_model", models.CharField(max_length=50)),
                ("created", models.DateTimeField()),
                ("current_sx_other", models.TextField()),
            ],
            options={
                "verbose_name": "Redmine #792.3: Signs and Symptoms: Possible list candidates",
                "verbose_name_plural": "Redmine #792.3: Signs and Symptoms: Possible list candidates",
                "db_table": "rm792_si_sx_list_candidates",
                "managed": False,
            },
        ),
    ]
