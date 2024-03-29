# Generated by Django 3.2 on 2022-09-30 11:06

from django.db import migrations, models
import django.db.models.deletion
import edc_action_item.managers
import edc_sites.models


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("effect_prn", "0011_auto_20220910_2045"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="hospitalization",
            managers=[
                ("on_site", edc_sites.models.CurrentSiteManager()),
                ("objects", edc_action_item.managers.ActionIdentifierModelManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="losstofollowup",
            managers=[
                ("on_site", edc_sites.models.CurrentSiteManager()),
                ("objects", edc_action_item.managers.ActionIdentifierModelManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="protocoldeviationviolation",
            managers=[
                ("on_site", edc_sites.models.CurrentSiteManager()),
                ("objects", edc_action_item.managers.ActionIdentifierModelManager()),
            ],
        ),
        migrations.AddField(
            model_name="historicalhospitalization",
            name="site",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="sites.site",
            ),
        ),
        migrations.AddField(
            model_name="hospitalization",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.site",
            ),
        ),
    ]
