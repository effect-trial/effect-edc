# Generated by Django 3.2 on 2022-08-24 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0086_auto_20220820_0823"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodresultschem",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsfbc",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultschem",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsfbc",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="historicalstudymedication",
            name="flucon_initiated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was the participant started on Fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedication",
            name="flucyt_dose",
            field=models.IntegerField(
                blank=True,
                help_text="Validate against weight and rando arm 100mg/kg, round down to nearest 500mg total e.g. 47kg = 4700mg, participant gets 4500mg daily",
                null=True,
                verbose_name="Flucytosine dose (mg)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedication",
            name="flucyt_initiated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                null=True,
                verbose_name="Was the participant started on Flucytosine?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedicationbaseline",
            name="flucon_initiated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was the participant started on Fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedicationbaseline",
            name="flucyt_dose",
            field=models.IntegerField(
                blank=True,
                help_text="Validate against weight and rando arm 100mg/kg, round down to nearest 500mg total e.g. 47kg = 4700mg, participant gets 4500mg daily",
                null=True,
                verbose_name="Flucytosine dose (mg)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedicationbaseline",
            name="flucyt_initiated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                null=True,
                verbose_name="Was the participant started on Flucytosine?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedicationfollowup",
            name="flucon_initiated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was the participant started on Fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedicationfollowup",
            name="flucyt_dose",
            field=models.IntegerField(
                blank=True,
                help_text="Validate against weight and rando arm 100mg/kg, round down to nearest 500mg total e.g. 47kg = 4700mg, participant gets 4500mg daily",
                null=True,
                verbose_name="Flucytosine dose (mg)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedicationfollowup",
            name="flucyt_initiated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                null=True,
                verbose_name="Was the participant started on Flucytosine?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalurinalysis",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="studymedication",
            name="flucon_initiated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was the participant started on Fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="studymedication",
            name="flucyt_dose",
            field=models.IntegerField(
                blank=True,
                help_text="Validate against weight and rando arm 100mg/kg, round down to nearest 500mg total e.g. 47kg = 4700mg, participant gets 4500mg daily",
                null=True,
                verbose_name="Flucytosine dose (mg)",
            ),
        ),
        migrations.AlterField(
            model_name="studymedication",
            name="flucyt_initiated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                null=True,
                verbose_name="Was the participant started on Flucytosine?",
            ),
        ),
        migrations.AlterField(
            model_name="urinalysis",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
