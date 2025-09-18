from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_UNKNOWN_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import IsDateEstimatedFieldNa
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start


class DeathReportModelMixin(models.Model):
    hospitalization_date = models.DateField(
        verbose_name="If YES, date of hospitalisation",
        validators=[date_not_future, date_not_before_study_start],
        null=True,
        blank=True,
    )

    hospitalization_date_estimated = IsDateEstimatedFieldNa(
        verbose_name="If YES, is this date estimated?",
        default=NOT_APPLICABLE,
    )

    clinical_notes_available = models.CharField(
        verbose_name="If died as inpatient, are clinical notes available to study staff?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If YES, include details of admission in narrative",
    )

    cm_sx = models.CharField(
        verbose_name=(
            "If YES, do notes document any symptoms or signs of "
            "cryptococcal meningitis prior to death?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    speak_nok = models.CharField(
        verbose_name="Did study staff speak to NOK following death?",
        max_length=5,
        choices=YES_NO,
        help_text="If YES, include other details of conversation in 'Next of kin narrative'",
    )

    date_first_unwell = models.DateField(
        verbose_name="If YES, when did they first become unwell?",
        validators=[date_not_future, date_not_before_study_start],
        null=True,
        blank=True,
    )

    date_first_unwell_estimated = IsDateEstimatedFieldNa(
        verbose_name="If YES, is this date estimated?",
        default=NOT_APPLICABLE,
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

    blurred_vision = models.CharField(
        verbose_name="If YES, did they complain of blurred vision?",
        max_length=25,
        choices=YES_NO_UNKNOWN_NA,
        blank=False,
        default=NOT_APPLICABLE,
    )

    nok_narrative = models.TextField(
        verbose_name="Next of kin narrative", blank=True, default=""
    )

    class Meta:
        abstract = True
