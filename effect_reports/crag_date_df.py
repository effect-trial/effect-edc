from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django_pandas.io import read_frame
from edc_utils import get_utcnow

if TYPE_CHECKING:
    from effect_reports.models import CragDateConfirmation


class CragDateDf:

    def __init__(self):
        self.model_cls = django_apps.get_model("effect_screening.subjectscreening")

    def to_dataframe(self) -> pd.DataFrame:
        qs = self.model_cls.objects.filter(consented=1)
        df = read_frame(qs)
        df = df[
            [
                "subject_identifier",
                "site",
                "screening_identifier",
                "report_datetime",
                "serum_crag_date",
                "serum_crag_value",
            ]
        ]
        df = df.reset_index(drop=True)
        df["report_date"] = df["report_datetime"].dt.date
        df = df.drop(columns=["report_datetime"])

        sites = {obj.domain: obj.id for obj in Site.objects.all()}
        df["site"] = df["site"].map(sites)

        df["report_model"] = "effect_reports.cragdateconfirmation"
        return df

    def to_model(self) -> CragDateConfirmation:
        df = self.to_dataframe()
        self.model_cls.objects.all().delete()
        now = get_utcnow()
        data = [
            self.model_cls(
                subject_identifier=row["subject_identifier"],
                site_id=row["site"],
                screening_identifier=row["screening_identifier"],
                serum_crag_date=row["serum_crag_date"],
                report_model=row["report_model"],
                report_date=row["report_date"],
                created=now,
            )
            for _, row in df.iterrows()
        ]

        self.model_cls.objects.bulk_create(data)
