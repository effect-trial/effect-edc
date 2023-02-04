# Generated by Django 3.2 on 2022-09-10 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("edc_adverse_event", "0009_auto_20220907_0157"),
        ("effect_ae", "0010_auto_20220826_1549"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aefollowup",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="aeinitial",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="aesusar",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="aetmg",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="deathreport",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="deathreporttmg",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalaefollowup",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalaeinitial",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalaesusar",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalaetmg",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreport",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreporttmg",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicaldeathreporttmgsecond",
            name="tracking_identifier",
        ),
        migrations.AddField(
            model_name="aeinitial",
            name="ae_action_classification",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_adverse_event.aeactionclassification",
                verbose_name="Classification of action taken",
            ),
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="ae_action_classification",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_adverse_event.aeactionclassification",
                verbose_name="Classification of action taken",
            ),
        ),
        migrations.AlterField(
            model_name="aefollowup",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="aeinitial",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="aesusar",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="aetmg",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="deathreport",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="deathreporttmg",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="historicalaefollowup",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalaeinitial",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalaesusar",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalaetmg",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldeathreport",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldeathreporttmg",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldeathreporttmgsecond",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
    ]
