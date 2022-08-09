# Generated by Django 3.2.8 on 2022-05-10 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0058_auto_20220507_0553"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalsignsandsymptoms",
            name="cm_sx_bloods_taken_other",
        ),
        migrations.RemoveField(
            model_name="historicalsignsandsymptoms",
            name="cm_sx_lp_done",
        ),
        migrations.RemoveField(
            model_name="signsandsymptoms",
            name="cm_sx_bloods_taken",
        ),
        migrations.RemoveField(
            model_name="signsandsymptoms",
            name="cm_sx_bloods_taken_other",
        ),
        migrations.RemoveField(
            model_name="signsandsymptoms",
            name="cm_sx_lp_done",
        ),
        migrations.AlterField(
            model_name="historicalsignsandsymptoms",
            name="current_sx_gte_g3_other",
            field=models.TextField(
                blank=True,
                help_text="If more than one, separate each with a comma (,).",
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsignsandsymptoms",
            name="current_sx_other",
            field=models.TextField(
                blank=True,
                help_text="If more than one, separate each with a comma (,).",
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="signsandsymptoms",
            name="current_sx_gte_g3_other",
            field=models.TextField(
                blank=True,
                help_text="If more than one, separate each with a comma (,).",
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="signsandsymptoms",
            name="current_sx_other",
            field=models.TextField(
                blank=True,
                help_text="If more than one, separate each with a comma (,).",
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
    ]
