from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from effect_subject.constants import IF_ADMITTED_COMPLETE_REPORTS, IF_YES_COMPLETE_AE


class ReportingFieldsModelMixin(models.Model):
    reportable_as_ae = models.CharField(
        verbose_name="Are any of the above Grade 3 or above, and NEWLY reportable?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=IF_YES_COMPLETE_AE,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the participant been NEWLY admitted due to any of the above?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=IF_ADMITTED_COMPLETE_REPORTS,
    )

    class Meta:
        abstract = True
