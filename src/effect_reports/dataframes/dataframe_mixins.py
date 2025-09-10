from __future__ import annotations

import pandas as pd
from django.apps import apps as django_apps
from edc_pdutils.dataframes import get_crf


class BaselineVlDfMixin:
    """A dataframe that lists baseline VLs."""

    model: str = None

    def to_dataframe(self) -> pd.DataFrame:
        df = get_crf(
            "effect_subject.arvhistory",
            subject_visit_model="effect_subject.subjectvisit",
            normalize=False,
            localize=False,
        )
        keep_cols = [
            "id",
            "subject_identifier",
            "site_id",
            "visit_code_str",
            "visit_code_sequence",
            "has_viral_load_result",
            "viral_load_result",
            "viral_load_quantifier",
            "viral_load_date",
            "viral_load_date_estimated",
            "user_created",
            "user_modified",
            "created",
            "modified",
        ]
        df = df[keep_cols]
        df = df.reset_index(drop=True)
        return df

    def to_model(self, model: str | None = None) -> None:
        df = self.to_dataframe()

        model_cls = django_apps.get_model(model or "effect_reports.baselinevlall")
        model_cls.objects.all().delete()

        data = [
            model_cls(
                # identifier
                crf_id=row["id"],
                subject_identifier=row["subject_identifier"],
                site_id=row["site_id"],
                visit_code=row["visit_code_str"],
                visit_code_sequence=row["visit_code_sequence"],
                # data
                has_viral_load_result=row["has_viral_load_result"],
                viral_load_result=(
                    None if pd.isna(row["viral_load_result"]) else row["viral_load_result"]
                ),
                viral_load_quantifier=row["viral_load_quantifier"],
                viral_load_date=(
                    None if pd.isna(row["viral_load_date"]) else row["viral_load_date"]
                ),
                viral_load_date_estimated=row["viral_load_date_estimated"],
                # audit
                user_created=row["user_created"],
                user_modified=row["user_modified"],
                created=row["created"],
                modified=row["modified"],
            )
            for _, row in df.iterrows()
        ]
        model_cls.objects.bulk_create(data)
