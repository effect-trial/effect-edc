import sys
from pathlib import Path

import pandas as pd
from clinicedc_constants import NO, NOT_APPLICABLE, UNKNOWN, YES
from django_pandas.io import read_frame
from pandas import Series

from effect_lists.models import ArvRegimens
from effect_prn.models import ArvSummary

COLUMN_MAP: dict[str, str] = {
    "PID": "subject_identifier",
    "Date of screening": "screening_date",
    "Unnamed: 2": "site_id",
    "Date of enrolment": "enrolment_date",
    "Was the ppt on ART at time of screening?": "at_screening",
    "Most recent regimen according to EDC": "current_regimen",
    "If YES, what was their ART regimen at time of screening?": "at_screening_regimen",
    "If other drugs at screening not listed, please specify here": (
        "at_screening_regimen_other"
    ),
    "When was this regimen MOST RECENTLY started or restarted?": (
        "at_screening_regimen_start_date"
    ),
    "Was ART coninued at enrolment": "cont_enrol",
    "If ART stopped at enrolment, or not on ART, what regimen was subsequently started?": (
        "cont_enrol_regimen"
    ),
    "If other drugs at enrolment not listed, please specify here": "cont_enrol_regimen_other",
    "Date of new regimen start/ re-start": "cont_enrol_regimen_start_date",
}

DROP_COLUMNS: list[str] = [
    "Date of screening",
    "Date of enrolment",
    "Unnamed: 2",
    "Most recent regimen according to EDC",
    "Was this regimen started or restarted within the last 30 days?",
    "Why did the ppt start or restart this regimen?",
    "If other reason not listed, please specify here…",
    "How long was the ppt on ART at time of enrolment?",
    "Was ART started <14 days before enrolment?",
    "Is there an HIVVL result available for this ppt pre-enrolment?",
    "HIVVL date",
    "Is this a recent HIVVL result? (<3 months pre-enrolment)",
    "Viral load value",
    "Decision made on ART at enrolment",
    "If ART stopped at enrolment, why?",
    "If other reason not listed, please specify here….1",
    "Is there a day 1 clinical note in the EDC?",
    "Day 1 clinical note narrative as per EDC",
    "Is there a day 15 clinical note in the EDC?",
    "Day 15 clinical note narrative as per EDC",
    "Unnamed: 31",
    "REMAINING QUERIES 20260525",
    "Site comments",
]


class ScriptError(Exception):
    def __init__(self):
        self.message = "ArvSummary records exist. Set delete_all=True to delete all records."


def at_screening_regimen_start_date_known(row) -> str:
    value = YES
    if row["at_screening"] == NO:
        value = NOT_APPLICABLE
    elif pd.isna(row["at_screening_regimen_start_date"]):
        value = NO
    return value


def cont_enrol(row) -> str:
    value = NO
    if (
        row["cont_enrol_orig"] == "Yes, regimen unchanged"
        or row["cont_enrol_orig"] == "Continued but regimen changed"
    ):
        value = YES
    elif row["at_screening"] == NO:
        value = NOT_APPLICABLE
    return value


def cont_enrol_regimen_changed(row) -> str:
    value = row["cont_enrol_orig"]
    if row["cont_enrol_orig"] == "Yes, regimen unchanged":
        value = NO
    elif row["cont_enrol_orig"] == "Continued but regimen changed":
        value = YES
    elif row["at_screening"] == NO:
        value = NOT_APPLICABLE
    return value


def cont_enrol_regimen_start_date_known(row) -> str:
    value = YES
    if row["cont_enrol_regimen_changed"] == NO:
        value = NOT_APPLICABLE
    elif pd.isna(row["cont_enrol_regimen_start_date"]):
        value = NO
    return value


def cont_enrol_ever_restarted(row) -> str:
    value = YES
    if row["cont_enrol_regimen"] == "ART not started or restarted by End of Study":
        value = NO
    elif row["cont_enrol_regimen"] == "Unknown":
        value = UNKNOWN
    elif row["cont_enrol"] == YES:
        value = NOT_APPLICABLE
    return value


def get_value(v):
    if pd.isna(v) or pd.isna(v):
        return None
    return v


def get_opts(row: Series, cols: list[str]):
    return {k: get_value(row[k]) for k in cols}


def run(path: str, delete_all: bool) -> None:
    """A script for a one-off import of ARV data collected
    manually in Excel.

    :param path: Path to Excel file.
    :param delete_all: Delete all records.
    :usage:
        uv run --no-dev --no-sources manage.py runscript \
            import_arv_summary_from_excel \
            --script-args "my/path" True \
            --settings=effect_edc.settings.live
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    sys.stdout.write(f"\n * Importing excel data from {path}\n")

    if ArvSummary.objects.all().count() > 0 and not delete_all:
        raise ScriptError()

    df = (
        pd.read_excel(path, sheet_name="ART details", skiprows=[1])
        .drop(columns=DROP_COLUMNS, errors="ignore")
        .rename(columns=COLUMN_MAP)
        .assign(site_id=lambda x: pd.to_numeric(x["site_id"], errors="coerce").astype("Int64"))
    )
    df = df[df["subject_identifier"] != "Example"].copy().reset_index(drop=True)

    cols = list(df.columns)
    cols[cols.index("at_screening_regimen")] = "at_screening_regimen_id"
    cols[cols.index("cont_enrol_regimen")] = "cont_enrol_regimen_id"

    df_regimens = read_frame(ArvRegimens.objects.all())
    df = (
        df.merge(
            df_regimens[["id", "name", "display_name"]],
            left_on="at_screening_regimen",
            right_on="display_name",
            how="left",
        )
        .rename(columns={"name": "at_screening_regimen_name", "id": "at_screening_regimen_id"})
        .drop(columns="display_name")
        .assign(
            at_screening_regimen_id=lambda x: pd.to_numeric(
                x["at_screening_regimen_id"], errors="coerce"
            ).astype("Int64")
        )
    )

    df = (
        df.merge(
            df_regimens[["id", "name", "display_name"]],
            left_on="cont_enrol_regimen",
            right_on="display_name",
            how="left",
        )
        .rename(columns={"name": "cont_enrol_regimen_name", "id": "cont_enrol_regimen_id"})
        .drop(columns="display_name")
        .assign(
            cont_enrol_regimen_id=lambda x: pd.to_numeric(
                x["cont_enrol_regimen_id"], errors="coerce"
            ).astype("Int64")
        )
        .assign(
            at_screening_regimen_start_date=lambda x: pd.to_datetime(
                x["at_screening_regimen_start_date"], errors="coerce"
            )
        )
        .assign(
            cont_enrol_regimen_start_date=lambda x: pd.to_datetime(
                x["cont_enrol_regimen_start_date"], errors="coerce"
            )
        )
    )

    df_ready = (
        df.fillna(
            value={
                "at_screening_regimen_other": "",
                "cont_enrol_regimen_other": "",
                "cont_enrol": "",
                "at_screening_regimen_start_date": None,
                "cont_enrol_regimen_start_date": None,
            }
        )
        .copy()
        .reset_index(drop=True)
    )

    df_ready["at_screening"] = df_ready["at_screening"].replace("yes", "Yes")

    df_ready["at_screening_regimen_start_date_known"] = pd.NA
    df_ready["at_screening_regimen_start_date_known"] = df_ready.apply(
        at_screening_regimen_start_date_known, axis=1
    )
    cols.append("at_screening_regimen_start_date_known")

    df_ready.loc[df_ready.subject_identifier == "106-110-0032-3", "cont_enrol"] = (
        "Yes, regimen unchanged"
    )

    df_ready["cont_enrol_orig"] = df_ready["cont_enrol"]

    df_ready["cont_enrol"] = df_ready.apply(cont_enrol, axis=1)

    df_ready["cont_enrol_regimen_changed"] = pd.NA
    df_ready["cont_enrol_regimen_changed"] = df_ready.apply(cont_enrol_regimen_changed, axis=1)
    cols.append("cont_enrol_regimen_changed")

    df_ready["cont_enrol_regimen_start_date_known"] = df_ready.apply(
        cont_enrol_regimen_start_date_known, axis=1
    )
    cols.append("cont_enrol_regimen_start_date_known")

    df_ready["cont_enrol_ever_restarted"] = ""

    df_ready["cont_enrol_ever_restarted"] = df_ready.apply(cont_enrol_ever_restarted, axis=1)
    cols.append("cont_enrol_ever_restarted")

    data = [ArvSummary(**get_opts(row, cols)) for _, row in df_ready.iterrows()]

    sys.stdout.write(f" * found {len(data)} records to create\n")
    sys.stdout.write(" * clearing ArvSummary table\n")
    recs = ArvSummary.objects.all().delete()
    sys.stdout.write(f" * deleted {recs} ArvSummary records\n")
    ArvSummary.objects.bulk_create(data)
    sys.stdout.write(f" * bulk created {ArvSummary.objects.count()} ArvSummary records\n")
    sys.stdout.write("Done\n")
