from clinicedc_constants import NULL_STRING
from clinicedc_constants.choices import YES_NO
from django.db import models
from django.utils import timezone
from edc_adverse_event.models import CauseOfDeath
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model_fields.fields import OtherCharField
from edc_sites.managers import CurrentSiteManager
from edc_sites.model_mixins import SiteModelMixin

CAUSE_TRIGGER_FIELDS = (
    "cause_of_death",
    "tmg_one_agrees",
    "tmg_one_cause_of_death",
    "tmg_two_agrees",
    "tmg_two_cause_of_death",
)


def get_death_values_to_copy(
    death_report: "DeathReport",  # noqa: F821
    tmg_one: "DeathReportTmg | None",  # noqa: F821
    tmg_two: "DeathReportTmgSecond | None",  # noqa: F821
) -> dict:
    """Values that DeathFinalCause copies from the source reports.

    Both TMG reports are optional. If absent, their copy columns are
    nulled so a subsequent refresh clears any stale data.
    """
    values = {
        "death_report": death_report,
        "death_report_action_identifier": death_report.action_identifier,
        "cause_of_death": death_report.cause_of_death,
        "cause_of_death_other": death_report.cause_of_death_other or "",
    }
    if tmg_one is None:
        values.update(
            {
                "tmg_one": None,
                "tmg_one_action_identifier": None,
                "tmg_one_cause_of_death": None,
                "tmg_one_cause_of_death_other": "",
                "tmg_one_agrees": "",
            }
        )
    else:
        values.update(
            {
                "tmg_one": tmg_one,
                "tmg_one_action_identifier": tmg_one.action_identifier,
                "tmg_one_cause_of_death": tmg_one.cause_of_death,
                "tmg_one_cause_of_death_other": tmg_one.cause_of_death_other or "",
                "tmg_one_agrees": tmg_one.cause_of_death_agreed,
            }
        )
    if tmg_two is None:
        values.update(
            {
                "tmg_two": None,
                "tmg_two_action_identifier": None,
                "tmg_two_cause_of_death": None,
                "tmg_two_cause_of_death_other": "",
                "tmg_two_agrees": "",
            }
        )
    else:
        values.update(
            {
                "tmg_two": tmg_two,
                "tmg_two_action_identifier": tmg_two.action_identifier,
                "tmg_two_cause_of_death": tmg_two.cause_of_death,
                "tmg_two_cause_of_death_other": tmg_two.cause_of_death_other or "",
                "tmg_two_agrees": tmg_two.cause_of_death_agreed,
            }
        )
    return values


def refresh_death_copies_from_sources(
    dfc: "DeathFinalCause",
    death_report: "DeathReport",  # noqa: F821
    tmg_one: "DeathReportTmg | None",  # noqa: F821
    tmg_two: "DeathReportTmgSecond | None",  # noqa: F821
) -> list[str]:
    """Refresh copy fields on `dfc` from its source records.

    If any of the cause-of-death trigger fields change (``cause_of_death``,
    ``tmg_one_cause_of_death``, ``tmg_two_cause_of_death``), ``final_cause_of_death``
    is cleared so the investigator is forced to reassess. Returns the list
    of fields written (empty list if nothing changed).
    """
    values = get_death_values_to_copy(death_report, tmg_one, tmg_two)
    changed = {f: v for f, v in values.items() if getattr(dfc, f) != v}
    if not changed:
        return []
    classification_changed = any(f in changed for f in CAUSE_TRIGGER_FIELDS)
    if classification_changed and dfc.final_cause_of_death_id is not None:
        changed["final_cause_of_death"] = None
        changed["final_cause_of_death_other"] = NULL_STRING
        changed["verified"] = False
    for f, v in changed.items():
        setattr(dfc, f, v)
    dfc.save(update_fields=list(changed))
    return list(changed)


class ModelManager(models.Manager):
    use_in_migrations = True


class DeathFinalCause(NonUniqueSubjectIdentifierModelMixin, SiteModelMixin, BaseUuidModel):
    """An investigator form completed after study closure
    to capture an agreed final cause of death.
    """

    report_datetime = models.DateTimeField(default=timezone.now)

    final_cause_of_death = models.ForeignKey(
        CauseOfDeath,
        on_delete=models.PROTECT,
        verbose_name="Final cause of death",
        null=True,
        blank=False,
    )

    final_cause_of_death_other = OtherCharField(max_length=250)

    verified = models.BooleanField(default=False)

    death_report = models.ForeignKey("DeathReport", on_delete=models.PROTECT, related_name="+")

    death_report_action_identifier = models.CharField(max_length=25, unique=True)

    # copied from effect_ae.deathreport
    cause_of_death = models.ForeignKey(
        CauseOfDeath,
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name="Original cause of death",
        help_text="Copied from original Death report",
    )

    # copied from effect_ae.deathreport
    cause_of_death_other = OtherCharField(
        verbose_name="Original cause of death (Other)",
        max_length=250,
        help_text="Copied from original Death report",
    )

    tmg_one = models.ForeignKey(
        "DeathReportTmg",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        help_text="May be null if no Death Report TMG report has been submitted yet.",
    )

    tmg_one_action_identifier = models.CharField(
        max_length=25,
        unique=True,
        null=True,
        blank=True,
    )

    # copied from effect_ae.deathreporttmg
    tmg_one_cause_of_death = models.ForeignKey(
        CauseOfDeath,
        related_name="+",
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Investigator 1 cause of death",
        help_text="Copied from the Death Report TMG (1)",
    )

    # copied from effect_ae.deathreporttmg
    tmg_one_cause_of_death_other = OtherCharField(
        verbose_name="Investigator 1 cause of death (Other)",
        max_length=250,
        default=NULL_STRING,
        help_text="Copied from the Death Report TMG (1)",
    )

    # copied from effect_ae.deathreporttmg
    tmg_one_agrees = models.CharField(
        verbose_name=(
            "TMG investigator one agrees with cause of death from the original death report?"
        ),
        max_length=15,
        choices=YES_NO,
        default=NULL_STRING,
    )

    tmg_two = models.ForeignKey(
        "DeathReportTmgSecond",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        help_text="May be null if no Death Report TMG (Second) report has been submitted yet.",
    )

    tmg_two_action_identifier = models.CharField(
        max_length=25,
        unique=True,
        null=True,
        blank=True,
    )

    # copied from effect_ae.deathreporttmgsecond
    tmg_two_cause_of_death = models.ForeignKey(
        CauseOfDeath,
        verbose_name="Investigator 2 cause of death",
        related_name="+",
        null=True,
        on_delete=models.PROTECT,
        help_text="Copied from the Death Report TMG (2)",
    )

    # copied from effect_ae.deathreporttmgsecond
    tmg_two_cause_of_death_other = OtherCharField(
        verbose_name="Investigator 2 cause of death (Other)",
        max_length=250,
        default=NULL_STRING,
        help_text="Copied from the Death Report TMG (2)",
    )

    # copied from effect_ae.deathreporttmgsecond
    tmg_two_agrees = models.CharField(
        verbose_name=(
            "TMG investigator two agrees with cause of death from the original death report?"
        ),
        max_length=15,
        choices=YES_NO,
        default=NULL_STRING,
    )

    objects = ModelManager()

    on_site = CurrentSiteManager()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.subject_identifier}: DeathReport-{self.death_report}"

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Death: Final cause of death"
        verbose_name_plural = "Death: Final cause of death"
