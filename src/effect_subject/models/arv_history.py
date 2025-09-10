from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_lab.choices import VL_QUANTIFIER_NA
from edc_model import models as edc_models
from edc_model.validators import date_not_future
from edc_reportable import CELLS_PER_MICROLITER

from effect_lists.models import ArvRegimens

from ..choices import ARV_DECISION, YES_NO_DEFAULTED_NA
from ..model_mixins import CrfModelMixin


class ArvHistory(CrfModelMixin, edc_models.BaseUuidModel):
    hiv_dx_date = models.DateField(
        verbose_name="Date HIV diagnosis first known",
        validators=[date_not_future],
        null=True,
        blank=False,
    )

    hiv_dx_date_estimated = edc_models.IsDateEstimatedField(
        verbose_name="Is this date estimated?"
    )

    on_art_at_crag = models.CharField(
        verbose_name=mark_safe(
            "Was the participant on ART <u>at time of</u> CrAg test?"
        ),  # nosec #B703 # B308
        max_length=5,
        choices=YES_NO,
        help_text=(
            "Also applies if ART started on the day of CrAg test (Test and Treat) "
            "or since CrAg test, but before enrolment."
        ),
    )

    ever_on_art = models.CharField(
        verbose_name=mark_safe(
            "Was the participant on ART <u>prior</u> to CrAg test?"
        ),  # nosec #B703 # B308
        max_length=5,
        choices=YES_NO,
    )

    initial_art_date = models.DateField(
        verbose_name=mark_safe(
            "When did the participant <u>start</u> ART for the first time?"
        ),  # nosec #B703 # B308
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    initial_art_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="Is this ART start date estimated?",
        default=NOT_APPLICABLE,
    )

    initial_art_regimen = models.ManyToManyField(
        ArvRegimens,
        verbose_name=mark_safe(
            "Which drugs were prescribed for their <u>first</u> (or <u>only</u>) ART regimen?"
        ),  # nosec #B703 # B308
        related_name="initial_arv",
    )

    initial_art_regimen_other = edc_models.OtherCharField()

    has_switched_art_regimen = models.CharField(
        verbose_name=mark_safe(
            "Has the participant ever <u>switched</u> ART regimen?"
        ),  # nosec #B703 # B308
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    current_art_date = models.DateField(
        verbose_name=mark_safe(
            "If switched, when was their <u>current or most recent</u> " "ART regimen started?"
        ),  # nosec #B703 # B308
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    current_art_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If switched, is the current ART start date estimated?",
        default=NOT_APPLICABLE,
    )

    current_art_regimen = models.ManyToManyField(
        ArvRegimens,
        verbose_name="If switched, what is their current (or most recent) ART regimen?",
        related_name="current_arv",
    )

    current_art_regimen_other = edc_models.OtherCharField()

    has_defaulted = models.CharField(
        verbose_name=mark_safe(
            "Has the participant <u>now</u> defaulted from their <u>current</u> ART regimen?"
        ),  # nosec #B703 # B308
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="Defaulted means no ART for at least one month.",
    )

    defaulted_date = models.DateField(
        verbose_name=mark_safe(
            "If `defaulted`, on what date did they default "
            "from their <u>current</u> ART regimen?"
        ),  # nosec #B703 # B308
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    defaulted_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="Is the `defaulted` date estimated?", default=NOT_APPLICABLE
    )

    is_adherent = models.CharField(
        verbose_name=mark_safe(
            "If the participant is currently on ART, are they <u>adherent</u> to "
            "their <u>current</u> ART regimen?"
        ),  # nosec #B703 # B308
        max_length=10,
        choices=YES_NO_DEFAULTED_NA,
        default=NOT_APPLICABLE,
    )

    art_doses_missed = models.IntegerField(
        verbose_name="If not `adherent`, how many doses missed in the last month?",
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        null=True,
        blank=True,
    )

    art_decision = models.CharField(
        verbose_name=mark_safe(
            "What decision was made at enrolment regarding their <u>current</u> ART regimen?"
        ),  # nosec #B703 # B308
        max_length=25,
        choices=ARV_DECISION,
        default=NOT_APPLICABLE,
    )

    has_viral_load_result = models.CharField(
        verbose_name="Is the last viral load result available?",
        max_length=15,
        choices=YES_NO,
    )

    viral_load_result = models.IntegerField(
        verbose_name="Viral load result",
        validators=[MinValueValidator(1), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text="copies/mL",
    )

    viral_load_quantifier = models.CharField(
        max_length=10,
        choices=VL_QUANTIFIER_NA,
        null=True,
        help_text=(
            "If lower than detection limit (LDL), use '<' and enter "
            "the lab detection limit value above."
        ),
    )

    retired_viral_load_result = models.DecimalField(
        verbose_name=(
            "Viral load result "
            "(original `viral_load_result` DecimalField, retired/superseded in "
            "effect-edc 0.1.57 by `viral_load_result` IntegerField. "
            "See also #658)"
        ),
        validators=[MinValueValidator(1), MaxValueValidator(9999999)],
        decimal_places=3,
        max_digits=10,
        null=True,
        blank=True,
        help_text=(
            "copies/mL "
            "(original `viral_load_result` DecimalField, retired/superseded in "
            "effect-edc 0.1.57 by `viral_load_result` IntegerField. "
            "See also #658)"
        ),
    )

    viral_load_date = models.DateField(
        verbose_name="Viral load date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    viral_load_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="Is the viral load date estimated?",
        default=NOT_APPLICABLE,
    )

    cd4_value = models.IntegerField(
        verbose_name="CD4 result",
        validators=[MinValueValidator(1), MaxValueValidator(105)],
        null=True,
        blank=False,
        help_text=CELLS_PER_MICROLITER,
    )

    cd4_date = models.DateField(
        verbose_name="CD4 date",
        validators=[date_not_future],
        null=True,
        blank=False,
    )

    cd4_date_estimated = edc_models.IsDateEstimatedField(
        verbose_name="Is the CD4 date estimated?"
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "ARV History"
        verbose_name_plural = "ARV History"
