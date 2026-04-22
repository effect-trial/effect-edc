import contextlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from clinicedc_constants import OTHER, UNKNOWN, YES
from django.contrib.sites.models import Site
from django.core.management import BaseCommand, CommandError
from edc_action_item.models import ActionItem
from edc_adverse_event.constants import DEATH_REPORT_TMG_SECOND_ACTION
from edc_adverse_event.models import CauseOfDeath
from tqdm import tqdm

from effect_ae.models import DeathReport, DeathReportTmgSecond


class Command(BaseCommand):
    help = "Backfill DeathReportTmgSecond from XLSX."

    cause_of_death_max_length = 100

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            dest="path",
            default=None,
            help="Path / folder",
        )

        parser.add_argument(
            "--filename",
            dest="filename",
            default=None,
            help="XLS filename",
        )

    @staticmethod
    def get_site_id(row) -> int:
        return int(row["subject_identifier"][4:7])

    @staticmethod
    def get_action_item(row) -> ActionItem | None:
        with contextlib.suppress(ActionItem.DoesNotExist):
            return ActionItem.objects.get(
                subject_identifier=row["subject_identifier"],
                action_type__name=DEATH_REPORT_TMG_SECOND_ACTION,
            )
        return None

    @staticmethod
    def get_cause_of_death_agreed(obj) -> str:
        if (
            obj.cause_of_death.name == OTHER
            and obj.narrative == obj.death_report.cause_of_death.display_name
        ):
            return YES
        return UNKNOWN

    def handle(self, *args, **options):  # noqa: ARG002
        path = options["path"]
        if not path:
            raise CommandError("Please provide a path")  # noqa: TRY003
        path = Path(path).expanduser()

        filename = options["filename"]  # "pts_removed_from_per_protocol.xlsx"
        if not filename:
            raise CommandError("Please provide a filename")  # noqa: TRY003

        df_raw = (
            pd.read_excel(
                path / filename,
                usecols=[
                    "PID",
                    "Death Report Identifier",
                    "Cause of death- 2nd TMG reviewer",
                    "CM related?",
                    "Comments",
                    "2nd TMG reviewer",
                ],
            )
            .rename(
                columns={
                    "PID": "subject_identifier",
                    "Death Report Identifier": "partial_action_identifier",
                    "Cause of death- 2nd TMG reviewer": "tmg2_cause_of_death_other",
                    "CM related?": "tmg2_cryptococcal_relatedness",
                    "Comments": "tmg2_cryptococcal_relatedness_comment",
                    "2nd TMG reviewer": "tmg2_user_created",
                }
            )
            .replace("NaN", pd.NA)
            .replace("NaT", pd.NaT)
            .replace("No", "")
            .replace("No ", "")
            .replace(np.nan, pd.NA)
        )
        df_raw["tmg2_cause_of_death"] = OTHER
        df_raw["cause_of_death_agreed"] = UNKNOWN
        df_raw["site_id"] = df_raw.apply(self.get_site_id, axis=1)

        cause_of_death_other = CauseOfDeath.objects.get(name=OTHER)

        for _, row in tqdm(df_raw.iterrows(), total=len(df_raw)):
            if action_item := self.get_action_item(row):
                death_report = DeathReport.objects.get(
                    subject_identifier=row["subject_identifier"]
                )
                tmg2_cause_of_death_other = (
                    "see narrative"
                    if len(row["tmg2_cause_of_death_other"]) > self.cause_of_death_max_length
                    else row["tmg2_cause_of_death_other"]
                )
                try:
                    death_report_tmg2 = DeathReportTmgSecond.objects.get(
                        subject_identifier=row["subject_identifier"]
                    )
                except DeathReportTmgSecond.DoesNotExist:
                    obj = DeathReportTmgSecond(
                        subject_identifier=row["subject_identifier"],
                        action_item=action_item,
                        action_identifier=action_item.action_identifier,
                        death_report=death_report,
                        cause_of_death=cause_of_death_other,
                        cause_of_death_other=tmg2_cause_of_death_other,
                        cause_of_death_agreed=UNKNOWN,
                        narrative=tmg2_cause_of_death_other,
                        site=Site.objects.get(id=row["site_id"]),
                    )
                    obj.save_base()
                    tqdm.write(f"{row['subject_identifier']}: Create DeathReportTmgSecond.\n")

                else:
                    update_fields = [
                        "action_item",
                        "cause_of_death",
                        "cause_of_death_other",
                        "cause_of_death_agreed",
                        "narrative",
                    ]
                    death_report_tmg2.action_item = action_item
                    death_report_tmg2.cause_of_death = cause_of_death_other
                    death_report_tmg2.cause_of_death_other = tmg2_cause_of_death_other
                    death_report_tmg2.cause_of_death_agreed = UNKNOWN
                    death_report_tmg2.narrative = tmg2_cause_of_death_other
                    death_report_tmg2.save_base(update_fields=update_fields)
                    tqdm.write(f"{row['subject_identifier']}: Updated DeathReportTmgSecond.\n")

            else:
                tqdm.write(
                    f"Error: {row['subject_identifier']}: "
                    f"{row['partial_action_identifier']} "
                    "ActionItem matching query does not exist.\n"
                )

        DeathReportTmgSecond.objects.update(cause_of_death_agreed=UNKNOWN)
        for obj in DeathReportTmgSecond.objects.all():
            obj.cause_of_death_agreed = self.get_cause_of_death_agreed(obj)
            obj.save_base(update_fields=["cause_of_death_agreed"])

        sys.stdout.write("Done\n")
