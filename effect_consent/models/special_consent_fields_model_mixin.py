from django.db import models
from edc_constants.choices import YES_NO


class SpecialConsentFieldsModelMixin(models.Model):
    """These fields were added around 1 March 2024"""

    he_substudy = models.CharField(
        verbose_name="Does the ppt agree to participate in the Health Economics sub-study?",
        max_length=15,
        choices=YES_NO,
    )

    sample_storage = models.CharField(
        verbose_name="Does the ppt agree to storage of samples in-country?",
        max_length=15,
        choices=YES_NO,
    )

    sample_export = models.CharField(
        verbose_name="Does the ppt agree to export of stored samples internationally?",
        max_length=15,
        choices=YES_NO,
    )

    hcw_data_sharing = models.CharField(
        verbose_name=(
            "Does the ppt agree to sharing study information with "
            "their primary healthcare provider? "
        ),
        max_length=15,
        choices=YES_NO,
    )

    class Meta:
        abstract = True
