from django.db import models
from edc_constants.constants import CONFIRMED
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model.validators import date_not_future
from edc_qareports.model_mixins import NoteModelMixin

from ...choices import NOTE_STATUSES


class SerumCragDateNote(
    UniqueSubjectIdentifierFieldMixin,
    NoteModelMixin,
):
    """Model class to replace default `Note` model used with
    QA Report `Serum Crag Date` model.

    `serum_crag_date` is to replace the current `serum_crag_date`
    in the screening model.
    """

    status = models.CharField(max_length=25, default=CONFIRMED, choices=NOTE_STATUSES)

    # confirmed serum_crag_date
    serum_crag_date = models.DateField(
        verbose_name="Confirmed serum/plasma CrAg sample collection date",
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text=(
            "Please enter first collection date in episode. "
            "Test must have been performed within 21 days of screening."
        ),
    )

    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self._meta.verbose_name}: {self.subject_identifier}"

    class Meta(UniqueSubjectIdentifierFieldMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Redmine #488.2 - Serum Crag Date Note"
        verbose_name_plural = "Redmine #488.2 - Serum Crag Date Notes"
