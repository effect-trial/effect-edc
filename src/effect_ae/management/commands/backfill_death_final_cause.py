"""Backfill DeathFinalCause rows from their source reports.

DeathReport is the starting document; DeathReportTmg and
DeathReportTmgSecond are child actions that may or may not exist yet.
For each ``DeathReport`` this command ensures a skeleton
``DeathFinalCause`` exists with the read-only columns pre-filled from
the sources. If a TMG report is absent, the corresponding copy columns
are left null and ``final_death_cause`` is not autofilled.

``final_death_cause`` is autofilled only when:
  - both the death report and TMG (1) classifications are present,
    agree, and neither is ``OTHER``; or
  - the TMG investigator agreed (``cause_of_death_agreed == YES``) and
    the TMG classification is ``NOT_APPLICABLE`` (i.e. they accepted
    the original); or
  - the TMG agreed and the original cause is ``OTHER`` and the text
    resolves to a known ``CauseOfDeath`` entry.

Idempotent: re-running only creates rows for DeathReports that do not
already have one. With ``--update-copies`` existing rows are refreshed
from the sources; if ``cause_of_death`` or ``tmg_one_cause_of_death``
changes on refresh, the existing ``final_death_cause`` is cleared so
the investigator must reassess.

Usage::

    uv run manage.py backfill_death_final_cause [--dry-run] [--update-copies]
"""

import contextlib

from clinicedc_constants import NULL_STRING, OTHER, YES
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from edc_adverse_event.models import CauseOfDeath

from effect_ae.models import (
    DeathFinalCause,
    DeathReport,
    DeathReportTmg,
    DeathReportTmgSecond,
)
from effect_ae.models.death_final_cause import (
    CAUSE_TRIGGER_FIELDS,
    get_death_values_to_copy,
    refresh_death_copies_from_sources,
)


class Command(BaseCommand):
    help = (
        "Create DeathFinalCause rows from DeathReport (with optional linked "
        "DeathReportTmg / DeathReportTmgSecond). Auto-fills final_death_cause "
        "only when both sources agree and neither is OTHER."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would be created/updated without changing the database.",
        )
        parser.add_argument(
            "--update-copies",
            action="store_true",
            help=(
                "Also refresh copied columns on existing DeathFinalCause rows. "
                "If cause_of_death or tmg_one_cause_of_death changes, "
                "final_death_cause is cleared so the investigator must reassess."
            ),
        )

    def handle(
        self,
        *args,  # noqa: ARG002
        dry_run: bool = False,
        update_copies: bool = False,
        **options,  # noqa: ARG002
    ):
        created = 0
        updated = 0
        skipped = 0

        qs = DeathReport.objects.all().order_by("created")
        total = qs.count()
        self.stdout.write(f"Scanning {total} DeathReport row(s)...")

        for death_report_obj in qs.iterator():
            death_final_obj = self.get_death_final_cause(death_report_obj)
            tmg_one_obj = self.get_tmg_one(death_report_obj)
            tmg_two_obj = self.get_tmg_two(death_report_obj)

            if not death_final_obj:
                copy_values = get_death_values_to_copy(
                    death_report_obj, tmg_one_obj, tmg_two_obj
                )
                (
                    copy_values["final_cause_of_death"],
                    copy_values["final_cause_of_death_other"],
                    copy_values["verified"],
                ) = self.get_final_death_cause(death_report_obj, tmg_one_obj, tmg_two_obj)
                if dry_run:
                    tmg_one_desc = (
                        f"tmg_one={tmg_one_obj.action_identifier}"
                        if tmg_one_obj is not None
                        else "no tmg_one"
                    )
                    tmg_two_desc = (
                        f"tmg_two={tmg_two_obj.action_identifier}"
                        if tmg_two_obj is not None
                        else "no tmg_two"
                    )
                    self.stdout.write(
                        f"  + would create DeathFinalCause for subject "
                        f"{death_report_obj.subject_identifier} "
                        f"(death_report={death_report_obj.action_identifier}, "
                        f"{tmg_one_desc}, {tmg_two_desc})"
                    )
                    created += 1
                    continue
                with transaction.atomic():
                    DeathFinalCause.objects.create(
                        subject_identifier=death_report_obj.subject_identifier,
                        site_id=death_report_obj.site_id,
                        report_datetime=timezone.now(),
                        user_created="django",
                        **copy_values,
                    )
                created += 1
                self.stdout.write(
                    f"  + created DeathFinalCause for subject "
                    f"{death_report_obj.subject_identifier}"
                )
                continue

            if not update_copies:
                skipped += 1
                continue

            if dry_run:
                new_values = get_death_values_to_copy(
                    death_report_obj, tmg_one_obj, tmg_two_obj
                )
                diffs = {
                    f: v for f, v in new_values.items() if getattr(death_final_obj, f) != v
                }
                if not diffs:
                    skipped += 1
                    continue
                if (
                    any(f in diffs for f in CAUSE_TRIGGER_FIELDS)
                    and death_final_obj.final_cause_of_death_id is not None
                ):
                    diffs["final_cause_of_death"] = None
                    diffs["final_cause_of_death_other"] = NULL_STRING
                    diffs["verified"] = False
                self.stdout.write(
                    f"  ~ would update {', '.join(sorted(diffs))} on "
                    f"DeathFinalCause for subject "
                    f"{death_report_obj.subject_identifier}"
                )
                updated += 1
                continue

            changed = refresh_death_copies_from_sources(
                death_final_obj, death_report_obj, tmg_one_obj, tmg_two_obj
            )
            if not changed:
                skipped += 1
                continue
            updated += 1
            self.stdout.write(
                f"  ~ updated {', '.join(sorted(changed))} on "
                f"DeathFinalCause for subject {death_report_obj.subject_identifier}"
            )

        verb_c = "Would create" if dry_run else "Created"
        verb_u = "Would update" if dry_run else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{verb_c} {created}, {verb_u} {updated}, skipped {skipped} already-current."
            )
        )

    @staticmethod
    def get_tmg_one(death_report: DeathReport) -> DeathReportTmg | None:
        """Return the DeathReportTmg for this DeathReport, or None."""
        obj = None
        with contextlib.suppress(DeathReportTmg.DoesNotExist):
            obj = DeathReportTmg.objects.get(death_report=death_report)
        return obj

    @staticmethod
    def get_tmg_two(death_report: DeathReport) -> DeathReportTmgSecond | None:
        """Return the DeathReportTmgSecond for this DeathReport, or None."""
        obj = None
        with contextlib.suppress(DeathReportTmgSecond.DoesNotExist):
            obj = DeathReportTmgSecond.objects.get(death_report=death_report)
        return obj

    @staticmethod
    def get_death_final_cause(death_report: DeathReport) -> DeathFinalCause | None:
        """Return the DeathFinalCause instance or None."""
        obj = None
        with contextlib.suppress(DeathFinalCause.DoesNotExist):
            obj = DeathFinalCause.objects.get(death_report=death_report)
        return obj

    @staticmethod
    def _effective_cause(
        dr_cause: CauseOfDeath | None,
        tmg_obj: DeathReportTmg | None,
    ) -> CauseOfDeath | None:
        """Resolve the effective cause from a TMG report.

        When the investigator agreed with the original report
        (``cause_of_death_agreed == YES``) the TMG cause is recorded as
        NOT_APPLICABLE, meaning they accept the death-report cause.
        Treat that as equivalent to the DR cause.
        """
        if tmg_obj is None:
            return None
        if tmg_obj.cause_of_death_agreed == YES:
            return dr_cause
        return tmg_obj.cause_of_death

    @staticmethod
    def get_final_death_cause(
        death_report_obj: DeathReport,
        tmg_one_obj: DeathReportTmg | None,
        tmg_two_obj: DeathReportTmgSecond | None,
    ) -> tuple[CauseOfDeath | None, str, bool]:
        """Return the agreed final cause of death when all submitted documents agree.

        Workflow:
          - DR + TMG1 only: both must agree → verified
          - DR + TMG1 + TMG2: all three must agree → verified
            (TMG2 is only requested when TMG1 disagrees, so this is the
            resolution path when there was initial disagreement)

        ``cause_of_death_agreed == YES`` on a TMG means the investigator
        accepts the DR cause; the TMG ``cause_of_death`` will be NOT_APPLICABLE
        in that case and is resolved back to the DR cause for comparison.

        Returns (final_cause_obj, final_cause_other, verified).
        """
        cause_obj: CauseOfDeath | None = None
        cause_other: str = NULL_STRING
        verified: bool = False

        if tmg_one_obj is None:
            # Cannot verify without at least one TMG report.
            return cause_obj, cause_other, verified

        dr_cause = death_report_obj.cause_of_death
        tmg1_eff = Command._effective_cause(dr_cause, tmg_one_obj)
        tmg2_eff = Command._effective_cause(dr_cause, tmg_two_obj)

        # Build the list of all resolved causes that must agree.
        resolved = [dr_cause, tmg1_eff]
        if tmg_two_obj is not None:
            resolved.append(tmg2_eff)

        # All resolved causes must be present and identical.
        if any(c is None for c in resolved):
            return cause_obj, cause_other, verified
        unique = {c.pk for c in resolved}
        if len(unique) != 1:
            return cause_obj, cause_other, verified

        # Unanimous — dr_cause is the agreed value.
        agreed_cause = dr_cause

        if agreed_cause.name == OTHER:
            # All agreed the cause is OTHER; try to resolve the free-text to a
            # known CauseOfDeath entry. If it cannot be resolved the investigator
            # must manually set the final cause — verified stays False.
            try:
                cause_obj = CauseOfDeath.objects.get(
                    Q(name=death_report_obj.cause_of_death_other.lower())
                    | Q(display_name=death_report_obj.cause_of_death_other)
                )
                verified = True
            except CauseOfDeath.DoesNotExist:
                cause_other = death_report_obj.cause_of_death_other or NULL_STRING
        else:
            cause_obj = agreed_cause
            verified = True

        return cause_obj, cause_other, verified
