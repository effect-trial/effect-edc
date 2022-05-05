from django.db import models
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_protocol.validators import date_not_before_study_start


class DeathReportModelMixin(models.Model):

    speak_nok = models.CharField(
        verbose_name="Did study staff speak to NOK following death?",
        max_length=5,
        choices=YES_NO,
        help_text="If YES, include other details of conversation in 'Next of kin narrative'",
    )

    date_first_unwell = models.DateField(
        verbose_name="If YES, when did they first become unwell?",
        validators=[edc_models.date_not_future, date_not_before_study_start],
        null=True,
        blank=True,
    )

    date_first_unwell_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If YES, is this date estimated?", default=NOT_APPLICABLE
    )

    headache = models.CharField(
        verbose_name="If YES, did they complain of a headache during this illness?",
        max_length=25,
        choices=YES_NO_UNKNOWN_NA,
        default=NOT_APPLICABLE,
    )

    drowsy_confused_altered_behaviour = models.CharField(
        verbose_name="If YES, did they become drowsy, confused of have altered behaviour?",
        max_length=25,
        choices=YES_NO_UNKNOWN_NA,
        default=NOT_APPLICABLE,
    )

    seizures = models.CharField(
        verbose_name="If YES, did they have any seizures?",
        max_length=25,
        choices=YES_NO_UNKNOWN_NA,
        default=NOT_APPLICABLE,
    )

    nok_narrative = models.TextField(
        verbose_name="Next of kin narrative",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
