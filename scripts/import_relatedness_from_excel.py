import sys
from pathlib import Path

import pandas as pd
from clinicedc_constants import (
    DEFINITELY_RELATED,
    NOT_APPLICABLE,
    NOT_RELATED,
    POSSIBLY_RELATED,
    PROBABLY_RELATED,
    UNLIKELY_RELATED,
)
from tqdm import tqdm

from effect_ae.models import DeathFinalCause


def run(path: str) -> None:
    """A script for a one-off import of cryptococcal
    relatedness values manually collected for the final cause
    of death (DeathFinalCause) in Excel.

    :param path: Path to Excel file.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    sys.stdout.write(f"\n * Importing excel data from {path}\n")
    df = (
        pd.read_excel(path, sheet_name="Final cause of death")
        .drop(
            columns=["cause_of_death as captured in EDC", "cause_of_death_other"],
            errors="ignore",
        )
        .rename(
            columns={
                "PID": "subject_identifier",
                "Final CM relatedness": "cryptococcal_relatedness",
            }
        )
    )

    mapping = {
        "Not related": NOT_RELATED,
        "Unlikely related": UNLIKELY_RELATED,
        "Possibly related": POSSIBLY_RELATED,
        "Probably related": PROBABLY_RELATED,
        "Definitely related": DEFINITELY_RELATED,
        "Not applicable": NOT_APPLICABLE,
    }
    df["cryptococcal_relatedness"] = df["cryptococcal_relatedness"].replace(mapping)
    total = DeathFinalCause.objects.all().count()
    for obj in tqdm(DeathFinalCause.objects.all(), total=total):
        value = df.loc[
            df["subject_identifier"] == obj.subject_identifier
        ].cryptococcal_relatedness.to_numpy()[0]
        obj.cryptococcal_relatedness = value
        obj.save()
