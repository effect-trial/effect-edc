import sys
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

import numpy as np
import pandas as pd
from django.core.management import BaseCommand, CommandError
from django.db.models.signals import post_save
from django.utils import timezone
from edc_registration.models.signals import (
    update_registered_subject_from_model_on_post_save,
)
from edc_sites.exceptions import InvalidSiteForSubjectError
from tqdm import tqdm

from effect_consent.models import SubjectConsent
from effect_consent.models.signals import subject_consent_on_post_save
from effect_screening.models import SubjectScreening


@contextmanager
def subject_consent_signals_disconnected():
    handlers = [
        (
            update_registered_subject_from_model_on_post_save,
            "update_registered_subject_from_model_on_post_save",
        ),
        (
            subject_consent_on_post_save,
            "subject_consent_on_post_save",
        ),
    ]
    # Disconnect. dispatch_uid is sufficient; don't pass receiver.
    for _, uid in handlers:
        post_save.disconnect(dispatch_uid=uid)
    try:
        yield
    finally:
        # Reconnect with the same uid and weak=False that the modules use.
        for fn, uid in handlers:
            post_save.connect(fn, weak=False, dispatch_uid=uid)


class Command(BaseCommand):
    """This is a one-off command to fix data in SubjectScreening
    and SubjectConsent.

    K Murphy submitted data fixes on file screening_queries_KM_20260417.xlsx
    and this code reads that file and updates the SubjectScreening
    and SubjectConsent models.
    """

    help = "Import screening_queries_KM_20260417.xlsx"

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
            default="screening_queries_KM_20260417.xlsx",
            help="XLS filename",
        )

        parser.add_argument(
            "--code",
            dest="code",
            default=None,
            help="access code",
        )

    def handle(self, *args, **options):  # noqa: ARG002
        code = options["code"]
        if not code or code != "erikis":
            raise CommandError("Please provide the correct code")  # noqa: TRY003
        path = options["path"]
        if not path:
            raise CommandError("Please provide a path")  # noqa: TRY003

        filename = options["filename"]
        if not filename:
            raise CommandError("Please provide a filename")  # noqa: TRY003

        path = Path(path).expanduser() / filename

        sys.stdout.write(f"\nImporting corrections from {filename}\n")

        df_raw = self.get_sheet_one_df(path)

        df_raw2 = self.get_sheet_two_df(path)

        # merge 1 and 2
        sys.stdout.write("- merged data from 1 and 2\n")
        df_raw = df_raw.merge(
            df_raw2, left_on="subject_identifier", right_on="subject_identifier", how="outer"
        )

        sys.stdout.write("- Updating Screening data\n")
        self.update_from_sheet_one_and_two(df_raw)

        # get third sheet data
        df_raw3 = self.get_sheet_three_df(path)

        self.update_from_sheet_three(df_raw3)

        sys.stdout.write("\nDone\n")

    @staticmethod
    def get_sheet_one_df(path: Path) -> pd.DataFrame:
        sheet_name = "CD4 and CrAg parsed EvW"
        sys.stdout.write(f"- {f'XLS Sheet 1: {sheet_name}'}\n")
        usecols = [
            "subject_identifier",
            "cd4_value",
            "cd4_date",
            "crag_date",
        ]
        df_raw = pd.read_excel(path, sheet_name=sheet_name, usecols=usecols)
        df_raw = (
            df_raw.replace("NaN", pd.NA)
            .replace("NaT", pd.NaT)
            .replace("No", "")
            .replace("No ", "")
            .replace(np.nan, pd.NA)
            .replace("180-0059", "180-0059-9")
        )

        # cleanup rows values
        df_raw = df_raw[~df_raw.subject_identifier.isin(["200-0011-6", "200-0009-0"])]
        df_raw["cd4_value"] = df_raw["cd4_value"].replace("", pd.NA)
        df_raw["cd4_value"] = pd.to_numeric(df_raw["cd4_value"])
        df_raw["cd4_date"] = pd.to_datetime(df_raw["cd4_date"])
        df_raw["crag_date"] = pd.to_datetime(df_raw["crag_date"])
        return df_raw

    @staticmethod
    def get_sheet_two_df(path: Path) -> pd.DataFrame:
        # get second sheet data
        sheet_name2 = "LP, pregnancy test, HIV test"
        sys.stdout.write(f"- {f'XLS Sheet 2: {sheet_name2}'}\n")

        usecols2 = [
            "subject_identifier",
            "preg_test_date",
            "HIV_confirmed_date",
            "LP_date",
        ]

        df_raw2 = (
            pd.read_excel(path, sheet_name=sheet_name2, usecols=usecols2)
            .rename(
                columns={
                    "preg_test_date": "preg_test_date",
                    "HIV_confirmed_date": "hiv_confirmed_date",
                    "LP_date": "lp_date",
                }
            )
            .replace("NaN", pd.NA)
            .replace("NaT", pd.NaT)
            .replace("No", "")
            .replace("No ", "")
            .replace(np.nan, pd.NA)
            .replace("150-0002-0", "150-0002-2")
        )

        # cleanup rows values
        df_raw2["preg_test_date"] = pd.to_datetime(df_raw2["preg_test_date"])
        df_raw2["hiv_confirmed_date"] = pd.to_datetime(df_raw2["hiv_confirmed_date"])
        df_raw2["lp_date"] = pd.to_datetime(df_raw2["lp_date"])
        return df_raw2

    @staticmethod
    def get_sheet_three_df(path: Path) -> pd.DataFrame:
        sheet_name3 = "Demographics, consent"
        sys.stdout.write(f"- {f'XLS Sheet 3: {sheet_name3}'}\n")
        usecols3 = ["subject_identifier", "age_in_years", "initials", "Correct date/time"]
        df_raw3 = (
            pd.read_excel(path, sheet_name=sheet_name3, usecols=usecols3)
            .rename(columns={"Correct date/time": "consent_time"})
            .replace("NaN", pd.NA)
            .replace("NaT", pd.NaT)
            .replace("No", "")
            .replace("No ", "")
            .replace(np.nan, pd.NA)
            .replace("150-0002-0", "150-0002-2")
        )

        df_raw3["consent_time"] = pd.to_datetime(df_raw3["consent_time"], format="%H:%M:%S")
        df_raw3["age_in_years"] = pd.to_numeric(df_raw3["age_in_years"])
        return df_raw3

    @staticmethod
    def update_from_sheet_one_and_two(df_raw: pd.DataFrame) -> None:
        i = 0
        for _, row in tqdm(df_raw.iterrows(), total=len(df_raw)):
            update_fields = []
            try:
                obj = SubjectScreening.objects.get(
                    subject_identifier=f"106-{row['subject_identifier']}"
                )
            except SubjectScreening.DoesNotExist:
                i += 1
                sys.stdout.write(
                    f"{i} - Subject identifier {row['subject_identifier']} not found.\n"
                )
            else:
                obj.dm_comment = ""
                if row["cd4_value"] and not pd.isna(row["cd4_value"]):
                    update_fields.append("cd4_value")
                    try:
                        obj.cd4_value = int(Decimal(row["cd4_value"]))
                    except InvalidOperation:
                        obj.cd4_value = int(row["cd4_value"])
                    except TypeError:
                        tqdm.write(
                            f"{i} - TypeError: Subject identifier {row['subject_identifier']} "
                            "cd4_value={row['cd4_value']}\n"
                        )
                for col in [
                    "cd4_date",
                    "crag_date",
                    "preg_test_date",
                    "hiv_confirmed_date",
                    "lp_date",
                ]:
                    if row[col] and not pd.isna(row[col]):
                        update_fields.append(col)
                        setattr(obj, col, row[col])
                if update_fields:
                    update_fields.extend(["user_modified", "modified", "dm_comment"])
                    obj.user_modified = "erikvw"
                    obj.modified = timezone.now()
                    msg = ",".join(update_fields)
                    obj.dm_comment = (
                        f"{obj.dm_comment}\n-Raw data change of fields {msg} as per "
                        "kmurphy screening_queries_KM_20260417.xlsx. "
                        "Validation bypassed via save_base (signals still fire)."
                    )
                    obj.save_base(update_fields=update_fields, raw=False)

    def update_from_sheet_three(self, df_raw3: pd.DataFrame) -> None:
        sys.stdout.write("- Updating Screening data\n")
        i = 0
        df = df_raw3[~pd.isna(df_raw3.age_in_years)]
        for _, row in tqdm(df.iterrows(), total=len(df)):
            try:
                obj = SubjectScreening.objects.get(
                    subject_identifier=f"106-{row['subject_identifier']}"
                )
            except SubjectScreening.DoesNotExist:
                i += 1
                sys.stdout.write(
                    f"{i} - Subject identifier {row['subject_identifier']} not found.\n"
                )
            else:
                update_fields = ["age_in_years", "user_modified", "modified", "dm_comment"]
                obj.age_in_years = row["age_in_years"]
                obj.user_modified = "erikvw"
                obj.modified = timezone.now()
                msg = ",".join(update_fields)
                obj.dm_comment = (
                    f"{obj.dm_comment}\n-Raw data change of fields {msg} as per kmurphy "
                    "screening_queries_KM_20260417.xlsx. Validation bypassed via save_base "
                    "(signals still fire)."
                )
                obj.save_base(update_fields=update_fields, raw=False)

        sys.stdout.write("- Updating Consent data\n")
        i = 0
        with subject_consent_signals_disconnected():
            for _, row in tqdm(df_raw3.iterrows(), total=len(df_raw3)):
                try:
                    obj = SubjectConsent.objects.get(
                        subject_identifier=f"106-{row['subject_identifier']}"
                    )
                except SubjectConsent.DoesNotExist:
                    i += 1
                    tqdm.write(
                        f"{i} - Subject identifier {row['subject_identifier']} not found.\n"
                    )
                except SubjectConsent.MultipleObjectsReturned:
                    for obj in SubjectConsent.objects.filter(
                        subject_identifier=f"106-{row['subject_identifier']}"
                    ):
                        self.update_sheet_three_consent(obj, row, multiple_versions=True)
                else:
                    self.update_sheet_three_consent(obj, row)

    @staticmethod
    def update_sheet_three_consent(obj, row, multiple_versions: bool = False):
        update_fields = []
        if not pd.isna(row["initials"]):
            obj.initials = row["initials"]
            update_fields.append("initials")
        if not pd.isna(row["consent_time"]):
            if multiple_versions:
                tqdm.write(
                    f"{obj.subject_identifier}. More than one version found. "
                    "Consent_datetime not updated.\n"
                )
            else:
                naive = datetime.combine(
                    obj.consent_datetime.date(), row["consent_time"].time()
                )
                obj.consent_datetime = timezone.make_aware(
                    naive, timezone=obj.consent_datetime.tzinfo
                )
                update_fields.append("consent_datetime")
        if update_fields:
            update_fields.extend(["user_modified", "modified", "dm_comment"])
            obj.user_modified = "erikvw"
            obj.modified = timezone.now()
            msg = ",".join(update_fields)
            obj.dm_comment = (
                f"{obj.dm_comment}\n-Raw data change of fields {msg} as "
                "per kmurphy screening_queries_KM_20260417.xlsx. "
                "Validation bypassed via save_base (signals still fire)."
            )
            try:
                obj.save_base(update_fields=update_fields, raw=False)
            except InvalidSiteForSubjectError as e:
                tqdm.write(f"Subject identifier {row['subject_identifier']} error. {e}\n")
