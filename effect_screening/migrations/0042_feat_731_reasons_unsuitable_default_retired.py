# Generated by Django 4.2.6 on 2024-03-15 05:09

from django.db import migrations
from django.db.migrations import RunPython
from edc_constants.constants import QUESTION_RETIRED, YES
from edc_utils import get_utcnow
from tqdm import tqdm


def retire_unanswered_reasons_unsuitable(apps, schema_editor):
    model_cls = apps.get_model("effect_screening.subjectscreening")
    qs = model_cls.objects.all()
    total = qs.count()
    print(
        f"\nProcessing {total} Subject Screening instances setting "
        f"default (retired) reasons_unsuitable ..."
    )
    for obj in tqdm(qs, total=total):
        if obj.unsuitable_for_study != YES and obj.reasons_unsuitable == "":
            obj.reasons_unsuitable = QUESTION_RETIRED
            obj.modified = get_utcnow()
            obj.user_modified = __name__ if len(__name__) <= 50 else f"{__name__[:46]} ..."

            obj.save_base(
                update_fields=[
                    "reasons_unsuitable",
                    "modified",
                    "user_modified",
                ]
            )
            print(f" * Updating '{obj.screening_identifier}' to '{obj.reasons_unsuitable=}'.")

    print("Finished updating. Summary ...")
    print(f" * {model_cls.objects.filter(reasons_unsuitable=QUESTION_RETIRED).count()=}")
    print("Done.")


class Migration(migrations.Migration):

    dependencies = [
        (
            "effect_screening",
            "0041_alter_historicalsubjectscreening_reasons_unsuitable_and_more",
        ),
    ]

    operations = [RunPython(retire_unanswered_reasons_unsuitable)]
