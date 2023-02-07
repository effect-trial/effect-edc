# Generated by Django 3.2.11 on 2022-02-24 15:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0011_auto_20220224_1509"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalmicrobiology",
            old_name="sputum_culture_taken_date",
            new_name="sputum_culture_date",
        ),
        migrations.RenameField(
            model_name="microbiology",
            old_name="sputum_culture_taken_date",
            new_name="sputum_culture_date",
        ),
        migrations.RemoveField(
            model_name="historicalmicrobiology",
            name="sputum_culture_pos_description",
        ),
        migrations.RemoveField(
            model_name="microbiology",
            name="sputum_culture_pos_description",
        ),
        migrations.AlterField(
            model_name="historicalmicrobiology",
            name="sputum_culture_result",
            field=models.CharField(
                choices=[
                    ("POS", "MTB Positive"),
                    ("NEG", "MTB Negative"),
                    ("IND", "Indeterminate / contaminated"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=10,
                verbose_name="Culture results",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmicrobiology",
            name="sputum_genexpert_result",
            field=models.CharField(
                choices=[
                    ("POS", "MTB Positive"),
                    ("NEG", "MTB Negative"),
                    ("IND", "Indeterminate"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=45,
                verbose_name="Sputum Gene-Xpert results",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmicrobiology",
            name="urinary_lam_result_grade",
            field=models.CharField(
                choices=[
                    ("1", "1+ (low)"),
                    ("2", "2+"),
                    ("3", "3+"),
                    ("4", "4+"),
                    ("5", "5+ (high)"),
                    ("unknown", "Unknown / Grade not reported"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If Urinary LAM is positive, grade",
            ),
        ),
        migrations.AlterField(
            model_name="microbiology",
            name="sputum_culture_result",
            field=models.CharField(
                choices=[
                    ("POS", "MTB Positive"),
                    ("NEG", "MTB Negative"),
                    ("IND", "Indeterminate / contaminated"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=10,
                verbose_name="Culture results",
            ),
        ),
        migrations.AlterField(
            model_name="microbiology",
            name="sputum_genexpert_result",
            field=models.CharField(
                choices=[
                    ("POS", "MTB Positive"),
                    ("NEG", "MTB Negative"),
                    ("IND", "Indeterminate"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=45,
                verbose_name="Sputum Gene-Xpert results",
            ),
        ),
        migrations.AlterField(
            model_name="microbiology",
            name="urinary_lam_result_grade",
            field=models.CharField(
                choices=[
                    ("1", "1+ (low)"),
                    ("2", "2+"),
                    ("3", "3+"),
                    ("4", "4+"),
                    ("5", "5+ (high)"),
                    ("unknown", "Unknown / Grade not reported"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If Urinary LAM is positive, grade",
            ),
        ),
    ]
