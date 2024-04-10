# Generated by Django 4.2.6 on 2024-03-12 12:48

from django.db import migrations
from django.db.migrations import RunPython
from edc_constants.constants import DECEASED, NOT_APPLICABLE, OTHER, YES
from edc_utils import get_utcnow
from tqdm import tqdm

from effect_screening.constants import UNABLE_TO_CONTACT


def update_screening_unsuitable(apps, schema_editor):
    model_cls = apps.get_model("effect_screening.subjectscreening")
    qs = model_cls.objects.all()
    total = qs.count()
    print(f"\nProcessing {total} Subject Screening instances for unsuitable_reasons ...")
    for obj in tqdm(qs, total=total):
        if obj.reasons_unsuitable.lower() in [
            reason.lower()
            for reason in [
                "unable to contact patient.",
                "unable to contact patient",
                "unable to contact participant",
                "unable to contact",
                "cannot contact patient",
            ]
        ]:
            obj.unsuitable_reason = UNABLE_TO_CONTACT
            if obj.unsuitable_agreed == YES:
                obj.unsuitable_agreed = NOT_APPLICABLE  # see #731

        elif obj.reasons_unsuitable.lower() in [
            reason.lower()
            for reason in [
                "patient died prior to screening",
                "died prior to screening",
                "patient died prior to screening.",
            ]
        ]:
            obj.unsuitable_reason = DECEASED
            if obj.unsuitable_agreed == YES:
                obj.unsuitable_agreed = NOT_APPLICABLE  # see #731

        elif obj.reasons_unsuitable:
            obj.unsuitable_reason = OTHER
            obj.unsuitable_reason_other = obj.reasons_unsuitable

        if obj.unsuitable_reason and obj.unsuitable_reason != NOT_APPLICABLE:
            obj.modified = get_utcnow()
            obj.user_modified = __name__ if len(__name__) <= 50 else f"{__name__[:46]} ..."

            update_fields = [
                "unsuitable_reason",
                "modified",
                "user_modified",
            ]
            if obj.unsuitable_reason != OTHER:
                update_fields.append("unsuitable_agreed")
            else:
                update_fields.append("unsuitable_reason_other"),

            obj.save_base(update_fields=update_fields)

            print(
                f" * Updating '{obj.screening_identifier}' with '{obj.unsuitable_reason=}' "
                # f"from '{obj.reasons_unsuitable=}'"
            )

    print("Final `unsuitable_reason` DB update summary ...")
    print(f" * {model_cls.objects.filter(unsuitable_reason=UNABLE_TO_CONTACT).count()=}")
    print(f" * {model_cls.objects.filter(unsuitable_reason=DECEASED).count()=}")
    print(f" * {model_cls.objects.filter(unsuitable_reason=OTHER).count()=}")
    print("Done.")


class Migration(migrations.Migration):

    dependencies = [
        ("effect_screening", "0039_historicalsubjectscreening_unsuitable_reason_and_more"),
    ]

    operations = [RunPython(update_screening_unsuitable)]
