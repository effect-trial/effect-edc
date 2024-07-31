from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models
from django_crypto_fields.fields import EncryptedCharField
from edc_constants.choices import GENDER
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model.validators import date_not_future, datetime_not_future
from edc_protocol.research_protocol_config import ResearchProtocolConfig
from edc_protocol.validators import datetime_not_before_study_start
from edc_sites.model_mixins import SiteModelMixin


class ScreeningCragDateConfirmation(
    UniqueSubjectIdentifierFieldMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    history = HistoricalRecords()

    # Fields to display
    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[datetime_not_before_study_start, datetime_not_future],
        # null=True,
        blank=False,
        # default=get_utcnow,
        help_text="Date and time of report.",
    )

    screening_identifier = models.CharField(
        verbose_name="Screening ID",
        max_length=50,
        blank=False,
        unique=True,
    )

    subject_identifier = models.CharField(
        max_length=50,
        validators=[RegexValidator(ResearchProtocolConfig().subject_identifier_pattern)],
        blank=False,
        unique=True,
    )

    initials = EncryptedCharField(
        validators=[
            RegexValidator("[A-Z]{1,3}", "Invalid format"),
            MinLengthValidator(2),
            MaxLengthValidator(3),
        ],
        blank=False,
    )

    # hidden fields
    dob = models.DateField(
        verbose_name="Date of birth",
        validators=[date_not_future],
        null=True,
        blank=False,
        help_text="Hidden, used for validation/audit",
    )

    gender = models.CharField(
        choices=GENDER,
        null=True,
        blank=False,
        max_length=10,
        help_text="Hidden, used for validation/audit",
    )

    serum_crag_date = models.DateField(
        verbose_name="Serum/plasma CrAg sample collection date",
        validators=[date_not_future],
        null=True,
        blank=False,
        help_text="Hidden, used for validation/audit",
    )

    eligibility_datetime = models.DateTimeField(
        verbose_name="Serum/plasma CrAg sample collection date",
        validators=[date_not_future],
        null=True,
        blank=False,
        help_text="Hidden, used for validation/audit",
    )

    # fields used for confirmation
    confirmed_dob = models.DateField(
        verbose_name="Date of birth",
        validators=[date_not_future],
        null=True,
        blank=False,
    )

    confirmed_gender = models.CharField(
        choices=GENDER,
        null=True,
        blank=False,
        max_length=10,
    )

    confirmed_serum_crag_date = models.DateField(
        verbose_name="Confirmed serum/plasma CrAg sample collection date",
        validators=[date_not_future],
        null=True,
        blank=False,
        help_text="Test must have been performed within 21 days of screening.",
    )
    # note = models.TextField(null=True)

    # TODO: No further action required (confirmed, pending, unable to get + reason)

    def __str__(self):
        return f"{self.subject_identifier} / {self.screening_identifier}"

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Screening Crag Date Confirmation"
        verbose_name_plural = "Screening Crag Date Confirmations"
        indexes = BaseUuidModel.Meta.indexes
