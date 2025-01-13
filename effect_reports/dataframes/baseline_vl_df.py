from __future__ import annotations

from typing import TYPE_CHECKING

from edc_constants.constants import NO, YES

from .dataframe_mixins import BaselineVlDfMixin

if TYPE_CHECKING:
    import pandas as pd


class BaselineVlAllDf(BaselineVlDfMixin):
    """A dataframe that lists ALL collected baseline VLs.

    See `BaselineVlAllAdmin` admin class get_queryset.
    """

    model = "effect_reports.baselinevlall"


class BaselineVlMissingQuantifierDf(BaselineVlDfMixin):
    """A dataframe listing collected baseline VLs where a VL result has
    been entered, but no corresponding `viral_load_quantifier` has been
    set.

    See `BaselineVlMissingQuantifierAdmin` admin class get_queryset.
    """

    model = "effect_reports.baselinevlmissingquantifier"

    def to_dataframe(self) -> pd.DataFrame:
        df = super().to_dataframe()
        df = df[df["viral_load_quantifier"].isna()]
        df = df.reset_index(drop=True)
        return df


class BaselineVlDiscrepancyDf(BaselineVlDfMixin):
    """A dataframe listing collected baseline VLs where there are
    discrepancies around the responses to `has_viral_load_result` and
    the other related VL questions.

    See `BaselineVlDiscrepancyAdmin` admin class get_queryset.
    """

    model = "effect_reports.baselinevldiscrepency"

    def to_dataframe(self) -> pd.DataFrame:
        df = super().to_dataframe()
        df = df[
            (
                (df["has_viral_load_result"] == YES)
                & (
                    df["viral_load_result"].isna()
                    | (df["viral_load_quantifier"] == "Not applicable")
                    # | ~df["viral_load_quantifier"].isin([EQ, GT, LT])
                    | df["viral_load_date"].isna()
                    | (df["viral_load_date_estimated"] == "Not applicable")
                )
            )
            | (
                (df["has_viral_load_result"] == NO)
                & (
                    df["viral_load_result"].notna()
                    | (df["viral_load_quantifier"] != "Not applicable")
                    | df["viral_load_date"].notna()
                    | (df["viral_load_date_estimated"] != "Not applicable")
                )
            )
        ]
        df = df.reset_index(drop=True)
        return df
