from django.db import models
from edc_adverse_event.choices import STUDY_DRUG_RELATIONSHIP
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE

from ...choices import INPATIENT_STATUSES


class AeEffectModelMixin(models.Model):
    flucon_relation = models.CharField(
        verbose_name="Relationship to study drugs: Fluconazole:",
        max_length=25,
        choices=[
            (value, desc) for value, desc in STUDY_DRUG_RELATIONSHIP if value != NOT_APPLICABLE
        ],
    )

    flucyt_relation = models.CharField(
        verbose_name="Relationship to study drugs: Flucytosine:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
    )

    patient_admitted = models.CharField(
        verbose_name="Was the participant admitted?",
        max_length=15,
        choices=YES_NO,
    )

    date_admitted = models.DateField(
        # TODO: Validate
        verbose_name='If "Yes", please specify date of hospital admission:',
        null=True,
        blank=True,
    )

    inpatient_status = models.CharField(
        # TODO: Validate
        verbose_name="Inpatient status:",
        max_length=25,
        choices=INPATIENT_STATUSES,
    )

    date_discharged = models.DateField(
        # TODO: Validate
        verbose_name='If "Discharged", please specify date discharged:',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
