# Generated by Django 5.1.3 on 2024-12-10 12:06

from django.db import migrations
from tqdm import tqdm


class DataMigrationError(Exception):
    pass


def raise_if_vl_has_decimal(apps, schema_editor):
    model_cls = apps.get_model("effect_subject.arvhistory")
    qs = model_cls.objects.all()
    total = qs.count()

    print(
        f"\nChecking {total} Arv History instances for `viral_load_result` "
        "containing non-integer values ..."
    )
    for obj in tqdm(qs, total=total):
        if obj.viral_load_result and obj.viral_load_result % 1 != 0:
            raise DataMigrationError(
                "Expected all `viral_load_result` values to be "
                "(decimal representations of) whole numbers. "
                f"Got {obj} {obj.viral_load_result=}."
            )
    print("Done checking")


class Migration(migrations.Migration):
    """Note: Migrations effect_subject/migrations/0119-0123 are all
    related, and expected to be run together.  See also ticket #658.
    """

    dependencies = [
        ("effect_subject", "0118_alter_bloodresultschem_crp_units_and_more"),
    ]

    operations = [
        migrations.RunPython(raise_if_vl_has_decimal),
        migrations.RenameField(
            model_name="arvhistory",
            old_name="viral_load_result",
            new_name="retired_viral_load_result",
        ),
        migrations.RenameField(
            model_name="historicalarvhistory",
            old_name="viral_load_result",
            new_name="retired_viral_load_result",
        ),
    ]
