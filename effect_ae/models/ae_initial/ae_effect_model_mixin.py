from django.db import models
from edc_adverse_event.choices import STUDY_DRUG_RELATIONSHIP


class AeEffectModelMixin(models.Model):

    fluconazole_relation = models.CharField(
        verbose_name="Relationship to study drugs: Fluconazole:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
    )

    flucytosine_relation = models.CharField(
        verbose_name="Relationship to study drugs: Flucytosine:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
    )

    class Meta:
        abstract = True
