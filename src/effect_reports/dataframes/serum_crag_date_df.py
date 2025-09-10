import pandas as pd
from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django_pandas.io import read_frame
from edc_utils import get_utcnow


class SerumCragDateDf:
    """A dataframe that lists serum_crag_date for every consented
    subject.

    See `SerumCragDateAdmin` admin class get_queryset.
    """

    model = "effect_reports.serumcragdate"

    def __init__(self):
        self.subject_screening_model_cls = django_apps.get_model(
            "effect_screening.subjectscreening"
        )
        self.model_cls = django_apps.get_model(self.model)

    def to_dataframe(self) -> pd.DataFrame:
        qs = self.subject_screening_model_cls.objects.filter(consented=1)
        df = read_frame(qs)
        df = df[
            [
                "subject_identifier",
                "site",
                "screening_identifier",
                "serum_crag_date",
                "eligibility_datetime",
                "serum_crag_value",
            ]
        ]
        df = df.reset_index(drop=True)
        df["eligibility_date"] = df["eligibility_datetime"].dt.date
        df = df.drop(columns=["eligibility_datetime"])

        sites = {obj.domain: obj.id for obj in Site.objects.all()}
        df["site"] = df["site"].map(sites)

        df["report_model"] = self.model
        return df

    def to_model(self) -> None:
        self.model_cls.objects.all().delete()

        df = self.to_dataframe()
        now = get_utcnow()
        data = [
            self.model_cls(
                subject_identifier=row["subject_identifier"],
                site_id=row["site"],
                screening_identifier=row["screening_identifier"],
                serum_crag_date=row["serum_crag_date"],
                eligibility_date=row["eligibility_date"],
                serum_crag_value=row["serum_crag_value"],
                report_model=row["report_model"],
                created=now,
            )
            for _, row in df.iterrows()
        ]

        self.model_cls.objects.bulk_create(data)
