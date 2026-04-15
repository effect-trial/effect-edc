import re
import sys
from pathlib import Path

import pandas as pd
from django.core.exceptions import MultipleObjectsReturned
from django.core.management import BaseCommand, CommandError
from django.utils import timezone
from tqdm import tqdm

from effect_lists.models import MissedDoseResponsibility
from effect_prn.choices import MISSED_DOSE_RESPONSIBILITY
from effect_prn.constants import REMAIN_ON_STUDY_MODIFIED
from effect_prn.models import ProtocolDeviationViolation


def get_missed_dose_conditions(original_string: str | None) -> str:
    if not original_string:
        name = ""
    elif "induction" in original_string.lower():
        name = "MISSED_GT_2D_INDUCTION_RX"
    elif "consolidation" in original_string.lower():
        name = "MISSED_GT_14D_CONSOLIDATION_RX"
    elif "maintenance" in original_string.lower():
        name = "MISSED_GT_14D_MAINTENANCE_RX"
    elif "error" in original_string.lower():
        name = "ENROLLED_IN_ERROR"
    else:
        raise ValueError(original_string)
    return name


def extract_numbers(data: list[str]) -> list[list[int]]:
    return [
        # Find all occurrences of 1, 2, or 3 and convert them to integers
        [int(n) for n in re.findall(r"[123]", item)]
        for item in data
    ]


def get_missed_dose_responsibility(original_string: str) -> list[str]:
    if not original_string:
        names = ["Not applicable"]
    else:
        options = {1: "Study staff", 2: "Routine care staff", 3: "Participant error"}
        numbers = extract_numbers([str(original_string)])
        names = [[options[i] for i in sublist if i in options] for sublist in numbers]
    return names[0]


class Command(BaseCommand):
    help = "Import XLS with information on patients removed from per-protocol analysis."

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

    def handle(self, *args, **options):  # noqa: ARG002
        path = options["path"]
        if not path:
            raise CommandError("Please provide a path")  # noqa: TRY003

        filename = options["filename"]  # "pts_removed_from_per_protocol.xlsx"
        if not filename:
            raise CommandError("Please provide a filename")  # noqa: TRY003

        path = Path(path).expanduser() / filename
        df = pd.read_excel(path).rename(
            columns={
                "PID": "subject_identifier",
                "Site": "site_name",
                "Reason withdrawn from PP analysis": "missed_dose_conditions_orig",
                "How many/ of what/ when?": "missed_dose_count_summary",
                "Study staff (1), routine care staff (2) or participant (3) error": (
                    "missed_dose_responsibility"
                ),
                "Reasons given by ppts for missed induction doses": "missed_dose_reason",
                "PD/PV associated?": "action_identifier",
            }
        )
        responsibility_map = {v: k for k, v in dict(MISSED_DOSE_RESPONSIBILITY).items()}
        for _, row in tqdm(df.iterrows(), total=len(df)):
            try:
                obj = ProtocolDeviationViolation.objects.get(
                    subject_identifier=row["subject_identifier"],
                    action_required__name=REMAIN_ON_STUDY_MODIFIED,
                )
            except ProtocolDeviationViolation.DoesNotExist:
                sys.stdout.write(f"{row['subject_identifier']} not found\n")
            except MultipleObjectsReturned:
                sys.stdout.write(f"{row['subject_identifier']} has more than one record\n")
            else:
                obj.missed_dose_conditions = get_missed_dose_conditions(
                    row["missed_dose_conditions_orig"]
                )
                obj.missed_dose_reason = row["missed_dose_reason"]
                obj.missed_dose_count_summary = row["missed_dose_count_summary"]
                obj.modified = timezone.now()
                obj.user_modified = "erikvw"
                obj.save()
                obj.missed_dose_responsibility.clear()
                values_list = get_missed_dose_responsibility(row["missed_dose_responsibility"])
                for value in values_list:
                    list_obj = MissedDoseResponsibility.objects.get(
                        name=responsibility_map.get(value)
                    )
                    obj.missed_dose_responsibility.add(list_obj)
