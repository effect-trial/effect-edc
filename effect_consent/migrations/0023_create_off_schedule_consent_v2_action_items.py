# Generated by Django 4.2.11 on 2024-05-15 14:29

from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from django.db.migrations import RunPython
from edc_action_item.create_or_update_action_type import create_or_update_action_type
from edc_action_item.identifiers import ActionIdentifier
from edc_action_item.models import ActionItem, ActionType
from edc_consent import site_consents
from edc_consent.exceptions import NotConsentedError
from edc_utils import get_utcnow
from tqdm import tqdm

from effect_consent.action_items import ConsentUpdateV2Action


def create_consent_v2_action_items(apps, schema_editor):
    eos_model_cls = apps.get_model("effect_prn.endofstudy")
    eos_qs = eos_model_cls.objects.all()
    total = eos_qs.count()

    create_or_update_action_type(apps=apps, **ConsentUpdateV2Action.as_dict())
    action_type = ActionType.objects.get(name=ConsentUpdateV2Action.name)

    print(
        f"\nProcessing {total} off-schedule instances "
        f"to add '{action_type.name}' to off-schedule subjects who "
        f"haven't already consented to it ..."
    )
    for obj in tqdm(eos_qs, total=total):
        print(f" * Processing '{obj.subject_identifier}' ...")
        try:
            subject_consent = site_consents.get_consent_or_raise(
                subject_identifier=obj.subject_identifier,
                report_datetime=get_utcnow(),
            )
        except NotConsentedError:
            pass
        else:
            if subject_consent.version == "2":
                print(f" * Skipping '{obj.subject_identifier}'. Already consented to v2.")
                continue

        try:
            ActionItem.objects.get(
                subject_identifier=obj.subject_identifier,
                action_type=action_type,
                site_id=obj.site.id,
            )
        except ObjectDoesNotExist:
            print(f" * Creating '{action_type.name}' for '{obj.subject_identifier}'.")
            action_identifier = ActionIdentifier(site_id=obj.site.id).identifier
            action_item = ActionItem(
                subject_identifier=obj.subject_identifier,
                action_identifier=action_identifier,
                action_type=action_type,
                site_id=obj.site.id,
            )
            action_item.save()
        else:
            print(
                f" * Skipping '{obj.subject_identifier}'. {action_type.name} already exists."
            )
    print("Done.")


class Migration(migrations.Migration):

    dependencies = [
        ("effect_consent", "0022_create_consent_v2_action_items"),
    ]

    operations = [RunPython(create_consent_v2_action_items)]
