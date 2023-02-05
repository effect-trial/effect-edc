# Generated by Django 3.2.13 on 2022-07-29 16:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0083_auto_20220725_1324"),
    ]

    operations = [
        migrations.AddField(
            model_name="bloodresultschem",
            name="albumin_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="alp_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="alt_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="amylase_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="ast_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="creatinine_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="crp_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="egfr_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="ggt_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="magnesium_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="potassium_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="tbil_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="urea_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="uric_acid_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="haemoglobin_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_diff_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="neutrophil_diff_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="neutrophil_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="platelets_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="rbc_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="wbc_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="albumin_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="alp_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="alt_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="amylase_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="ast_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="creatinine_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="crp_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="egfr_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="ggt_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="magnesium_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="potassium_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="tbil_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="urea_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="uric_acid_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="haemoglobin_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_diff_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="neutrophil_diff_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="neutrophil_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="platelets_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="rbc_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="wbc_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalurinalysis",
            name="proteinuria_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="urinalysis",
            name="proteinuria_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultschem",
            name="alp_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultschem",
            name="alt_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultschem",
            name="amylase_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultschem",
            name="ast_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultschem",
            name="ggt_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultschem",
            name="alp_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultschem",
            name="alt_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultschem",
            name="amylase_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultschem",
            name="ast_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultschem",
            name="ggt_units",
            field=models.CharField(
                blank=True,
                choices=[("IU/L", "IU/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
    ]
