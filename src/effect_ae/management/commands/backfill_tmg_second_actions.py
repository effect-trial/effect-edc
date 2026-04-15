"""Backfill DEATH_REPORT_TMG_SECOND_ACTION action items.

For each existing ``DeathReportTmg`` that does not already have a
corresponding ``DEATH_REPORT_TMG_SECOND_ACTION`` child action item,
create one. Idempotent: re-running only touches rows that are still
missing the child action item.

Required because EFFECT schedules the second TMG review whenever the
first review exists (see ``EffectDeathReportTmgAction``), rather than
only when the first reviewer disagrees with the cause of death. Rows
created before that policy change won't have the child action item.

Usage::

    uv run manage.py backfill_tmg_second_actions [--dry-run]
"""

from django.core.management.base import BaseCommand
from edc_action_item.models import ActionItem
from edc_action_item.site_action_items import site_action_items
from edc_adverse_event.constants import DEATH_REPORT_TMG_SECOND_ACTION

from effect_ae.models import DeathReportTmg


class Command(BaseCommand):
    help = (
        "Create missing DEATH_REPORT_TMG_SECOND_ACTION action items for "
        "existing DeathReportTmg rows."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would be created without changing the database.",
        )

    def handle(self, *args, dry_run: bool = False, **options):  # noqa: ARG002
        action_cls = site_action_items.get(DEATH_REPORT_TMG_SECOND_ACTION)
        created = 0
        skipped = 0
        missing_parent = 0

        qs = DeathReportTmg.objects.all().order_by("created")
        total = qs.count()
        self.stdout.write(f"Scanning {total} DeathReportTmg row(s)...")

        for tmg in qs.iterator():
            try:
                parent_ai = ActionItem.objects.get(action_identifier=tmg.action_identifier)
            except ActionItem.DoesNotExist:
                missing_parent += 1
                self.stderr.write(
                    f"  ! no parent ActionItem for DeathReportTmg "
                    f"{tmg.action_identifier} (subject={tmg.subject_identifier}) -- skipped"
                )
                continue

            already = ActionItem.objects.filter(
                parent_action_item=parent_ai,
                action_type__name=DEATH_REPORT_TMG_SECOND_ACTION,
            ).exists()
            if already:
                skipped += 1
                continue

            if dry_run:
                self.stdout.write(
                    f"  + would create 2nd TMG action for subject "
                    f"{tmg.subject_identifier} (parent={tmg.action_identifier})"
                )
                created += 1
                continue

            action_cls(
                subject_identifier=tmg.subject_identifier,
                parent_action_item=parent_ai,
                related_action_item=parent_ai.related_action_item,
                skip_get_current_site=True,
                site_id=tmg.site_id,
            )
            created += 1
            self.stdout.write(
                f"  + created 2nd TMG action for subject "
                f"{tmg.subject_identifier} (parent={tmg.action_identifier})"
            )

        verb = "Would create" if dry_run else "Created"
        self.stdout.write(
            self.style.SUCCESS(
                f"{verb} {created} action item(s). "
                f"Skipped {skipped} already-present, {missing_parent} missing-parent."
            )
        )
