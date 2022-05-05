# Generated by Django 3.2.8 on 2022-04-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0041_auto_20220427_2246"),
    ]

    operations = [
        migrations.RenameField(
            model_name="adherence",
            old_name="any_fluconazole_doses_missed",
            new_name="fcon_doses_missed",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="fluconazole_doses_missed",
            new_name="fcon_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="any_flucytosine_doses_missed",
            new_name="fcyz_doses_missed",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="flucytosine_doses_missed",
            new_name="fcyz_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="receiving_arv_reason_no",
            new_name="on_arv_reason_no",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="receiving_fluconazole_reason_no",
            new_name="on_fcon_reason_no",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="opinion_art_adherent",
            new_name="opinion_arv_adherent",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="opinion_fluconazole_adherent",
            new_name="opinion_fcon_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="any_fluconazole_doses_missed",
            new_name="fcon_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="fluconazole_doses_missed",
            new_name="fcon_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="any_flucytosine_doses_missed",
            new_name="fcyz_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="flucytosine_doses_missed",
            new_name="fcyz_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="receiving_arv_reason_no",
            new_name="on_arv_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="receiving_fluconazole_reason_no",
            new_name="on_fcon_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="opinion_art_adherent",
            new_name="opinion_arv_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="opinion_fluconazole_adherent",
            new_name="opinion_fcon_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="any_fluconazole_doses_missed",
            new_name="fcon_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="fluconazole_doses_missed",
            new_name="fcon_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="any_flucytosine_doses_missed",
            new_name="fcyz_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="flucytosine_doses_missed",
            new_name="fcyz_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="receiving_arv_reason_no",
            new_name="on_arv_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="receiving_fluconazole_reason_no",
            new_name="on_fcon_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="opinion_art_adherent",
            new_name="opinion_arv_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="opinion_fluconazole_adherent",
            new_name="opinion_fcon_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="any_fluconazole_doses_missed",
            new_name="fcon_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="fluconazole_doses_missed",
            new_name="fcon_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="any_flucytosine_doses_missed",
            new_name="fcyz_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="flucytosine_doses_missed",
            new_name="fcyz_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="receiving_arv_reason_no",
            new_name="on_arv_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="receiving_fluconazole_reason_no",
            new_name="on_fcon_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="opinion_art_adherent",
            new_name="opinion_arv_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="opinion_fluconazole_adherent",
            new_name="opinion_fcon_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="any_fluconazole_doses_missed",
            new_name="fcon_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="fluconazole_doses_missed",
            new_name="fcon_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="any_flucytosine_doses_missed",
            new_name="fcyz_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="flucytosine_doses_missed",
            new_name="fcyz_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="receiving_arv_reason_no",
            new_name="on_arv_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="receiving_fluconazole_reason_no",
            new_name="on_fcon_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="opinion_art_adherent",
            new_name="opinion_arv_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="opinion_fluconazole_adherent",
            new_name="opinion_fcon_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="any_fluconazole_doses_missed",
            new_name="fcon_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="fluconazole_doses_missed",
            new_name="fcon_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="any_flucytosine_doses_missed",
            new_name="fcyz_doses_missed",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="flucytosine_doses_missed",
            new_name="fcyz_doses_missed_number",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="receiving_arv_reason_no",
            new_name="on_arv_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="receiving_fluconazole_reason_no",
            new_name="on_fcon_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="opinion_art_adherent",
            new_name="opinion_arv_adherent",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="opinion_fluconazole_adherent",
            new_name="opinion_fcon_adherent",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="receiving_arv",
            new_name="on_arv",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="receiving_fluconazole",
            new_name="on_fcon",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="receiving_arv",
            new_name="on_arv",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="receiving_fluconazole",
            new_name="on_fcon",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="receiving_arv",
            new_name="on_arv",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="receiving_fluconazole",
            new_name="on_fcon",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="receiving_arv",
            new_name="on_arv",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="receiving_fluconazole",
            new_name="on_fcon",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="receiving_arv",
            new_name="on_arv",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="receiving_fluconazole",
            new_name="on_fcon",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="receiving_arv",
            new_name="on_arv",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="receiving_fluconazole",
            new_name="on_fcon",
        ),
        migrations.AlterField(
            model_name="adherence",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient linked up with their local clinic?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherence",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient linked up with their local clinic?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagefour",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient linked up with their local clinic?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestageone",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient linked up with their local clinic?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagethree",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient linked up with their local clinic?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagetwo",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Has the patient linked up with their local clinic?",
            ),
        ),
    ]
