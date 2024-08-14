from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model.validators import date_not_future
from edc_qareports.model_mixins import NoteModelMixin


class ConfirmedSerumCragDate(
    UniqueSubjectIdentifierFieldMixin,
    NoteModelMixin,
):

    history = HistoricalRecords()

    confirmed_serum_crag_date = models.DateField(
        verbose_name="Confirmed serum/plasma CrAg sample collection date",
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text=(
            "Please enter first collection date in episode. "
            "Test must have been performed within 21 days of screening."
        ),
    )

    def __str__(self) -> str:
        return f"{self._meta.verbose_name}: {self.subject_identifier}"

    class Meta(UniqueSubjectIdentifierFieldMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Redmine #488.2 Confirmed Serum Crag Date"
        verbose_name_plural = "Redmine #488.2 Confirmed Serum Crag Dates"
