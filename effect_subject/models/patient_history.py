from ambition_lists.models import ArvRegimens, Medication, Neurological, Symptom
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE, QUESTION_RETIRED
from edc_constants.utils import append_question_retired_choice
from edc_model.models import HistoricalRecords, date_not_future
from edc_model_fields.fields import IsDateEstimatedFieldNa, OtherCharField
from edc_visit_tracking.managers import CrfModelManager

from ..choices import (
    ARV_DECISION,
    ECOG_SCORE,
    FIRST_ARV_REGIMEN,
    FIRST_LINE_REGIMEN,
    SECOND_ARV_REGIMEN,
    TB_SITE,
    WEIGHT_DETERMINATION,
)
from ..managers import CurrentSiteManager
from .crf_model_mixin import CrfModelMixin

FIRST_ARV_REGIMEN_RETIRED = append_question_retired_choice(FIRST_ARV_REGIMEN)
SECOND_ARV_REGIMEN_RETIRED = append_question_retired_choice(SECOND_ARV_REGIMEN)
FIRST_LINE_REGIMEN_RETIRED = append_question_retired_choice(FIRST_LINE_REGIMEN)
YES_NO_NA_RETIRED = append_question_retired_choice(YES_NO_NA)


class PatientHistory(CrfModelMixin):

    symptom = models.ManyToManyField(
        Symptom,
        blank=True,
        related_name="symptoms",
        verbose_name="What are your current symptoms?",
    )

    headache_duration = models.IntegerField(
        verbose_name="If headache, how many days did it last?",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    visual_loss_duration = models.IntegerField(
        verbose_name="If visual loss, how many days did it last?",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    # retired
    first_arv_regimen = models.CharField(
        verbose_name="If YES, which drugs were prescribed for their first ART regimen?",
        max_length=50,
        choices=FIRST_ARV_REGIMEN_RETIRED,
        default=QUESTION_RETIRED,
        editable=False,
    )

    # retired
    first_arv_regimen_other = OtherCharField(editable=False)

    # retired
    first_line_choice = models.CharField(
        verbose_name="If first line:",
        max_length=25,
        choices=FIRST_LINE_REGIMEN_RETIRED,
        default=QUESTION_RETIRED,
        editable=False,
    )

    current_arv_decision = models.CharField(
        verbose_name=mark_safe(
            "What decision was made at admission regarding their "
            "<u>current</u> ART regimen?"
        ),
        max_length=25,
        choices=ARV_DECISION,
        default=NOT_APPLICABLE,
    )

    # retired
    second_arv_regimen = models.CharField(
        verbose_name="Second line ARV regimen",
        max_length=50,
        choices=SECOND_ARV_REGIMEN_RETIRED,
        default=QUESTION_RETIRED,
        editable=False,
    )

    # retired
    second_arv_regimen_other = OtherCharField(editable=False)

    # retired
    patient_adherence = models.CharField(
        verbose_name="Is the patient reportedly adherent?",
        max_length=25,
        choices=YES_NO_NA_RETIRED,
        default=QUESTION_RETIRED,
        editable=False,
    )

    # retired
    last_dose = models.IntegerField(
        verbose_name=(
            "If no tablets taken this month, how many months "
            "since the last dose taken?"
        ),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        editable=False,
    )

    temp = models.DecimalField(
        verbose_name="Temperature:",
        validators=[MinValueValidator(30), MaxValueValidator(45)],
        decimal_places=1,
        max_digits=3,
        help_text="in degrees Celcius",
    )

    heart_rate = models.IntegerField(
        verbose_name="Heart rate:",
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        help_text="bpm",
    )

    sys_blood_pressure = models.IntegerField(
        verbose_name="Blood pressure: systolic",
        validators=[MinValueValidator(50), MaxValueValidator(220)],
        help_text="in mm. format SYS, e.g. 120",
    )

    dia_blood_pressure = models.IntegerField(
        verbose_name="Blood pressure: diastolic",
        validators=[MinValueValidator(20), MaxValueValidator(150)],
        help_text="in Hg. format DIA, e.g. 80",
    )

    respiratory_rate = models.IntegerField(
        verbose_name="Respiratory rate:",
        validators=[MinValueValidator(6), MaxValueValidator(50)],
        help_text="breaths/min",
    )

    weight = models.DecimalField(
        verbose_name="Weight:",
        validators=[MinValueValidator(20), MaxValueValidator(150)],
        decimal_places=1,
        max_digits=4,
        help_text="kg",
    )

    weight_determination = models.CharField(
        verbose_name="Is weight estimated or measured?",
        max_length=15,
        choices=WEIGHT_DETERMINATION,
    )

    glasgow_coma_score = models.IntegerField(
        verbose_name="Glasgow Coma Score:",
        validators=[MinValueValidator(3), MaxValueValidator(15)],
        help_text="/15",
    )

    neurological = models.ManyToManyField(Neurological, blank=True)

    neurological_other = OtherCharField(
        verbose_name='If "Other CN palsy", specify',
        max_length=250,
        blank=True,
        null=True,
    )

    focal_neurologic_deficit = models.TextField(
        verbose_name='If "Focal neurologic deficit" chosen, please specify details:',
        null=True,
        blank=True,
    )

    visual_acuity_day = models.DateField(
        verbose_name="Study day visual acuity recorded?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    left_acuity = models.DecimalField(
        verbose_name="Visual acuity left eye:",
        decimal_places=3,
        max_digits=4,
        null=True,
        blank=True,
    )

    right_acuity = models.DecimalField(
        verbose_name="Visual acuity right eye",
        decimal_places=3,
        max_digits=4,
        null=True,
        blank=True,
    )

    ecog_score = models.CharField(
        verbose_name="ECOG Disability Score", max_length=15, choices=ECOG_SCORE
    )

    ecog_score_value = models.CharField(
        verbose_name="ECOG Score", max_length=15, choices=ECOG_SCORE
    )

    lung_exam = models.CharField(
        verbose_name="Abnormal lung exam:", max_length=5, choices=YES_NO
    )

    cryptococcal_lesions = models.CharField(
        verbose_name="Cryptococcal related skin lesions:", max_length=5, choices=YES_NO
    )

    specify_medications = models.ManyToManyField(Medication, blank=True)

    specify_medications_other = models.TextField(max_length=150, blank=True, null=True)

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Patient's History"
        verbose_name_plural = "Patient's History"
