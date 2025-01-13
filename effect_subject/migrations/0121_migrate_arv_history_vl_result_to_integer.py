# Generated by Django 5.1.3 on 2025-01-10 16:30

from django.db import migrations
from edc_utils import get_utcnow, truncate_string
from simple_history.utils import update_change_reason
from tqdm import tqdm

from effect_subject.models import ArvHistory
from effect_subject.utils import get_max_field_len


def migrate_retired_vl_result_to_vl_result(apps, schema_editor):
    # Prepare qs
    # model_cls = apps.get_model("effect_subject.arvhistory")
    model_cls = ArvHistory
    qs = model_cls.objects.filter(retired_viral_load_result__isnull=False)
    total = qs.count()

    # Prepare history
    user_modified = truncate_string(
        string=__name__,
        max_length=get_max_field_len(model_cls, "user_modified"),
    )
    change_reason = truncate_string(
        string=f"Migrated `viral_load_result` from DecimalField to IntegerField. See: {__name__}",
        max_length=get_max_field_len(model_cls.history.model, "history_change_reason"),
    )

    # Perform data migration
    print(
        f"\nMigrating {total} Arv History `retired_viral_load_result` "
        "to `viral_load_result` ..."
    )
    for obj in tqdm(qs, total=total):
        obj.viral_load_result = int(obj.retired_viral_load_result)
        obj.modified = get_utcnow()
        obj.user_modified = user_modified
        obj.save()
        update_change_reason(instance=obj, reason=change_reason)
        print(
            f"Migrated {obj} vl from {obj.retired_viral_load_result:>10} "
            f"to {obj.viral_load_result}"
        )
    print("Done migrating")


class Migration(migrations.Migration):
    """Note: Migrations effect_subject/migrations/0119-0123 are all
    related, and expected to be run together.  See also ticket #658.
    """

    dependencies = [
        ("effect_subject", "0120_arvhistory_viral_load_quantifier_and_more"),
    ]

    operations = [
        migrations.RunPython(migrate_retired_vl_result_to_vl_result),
    ]
