"""Signals that keep AeFinalClassification copy fields in sync with
their source records (AeInitial, AeTmg).

When either source is saved, any AeFinalClassification row linked to
it has its copy fields refreshed. If the refresh changes
`ae_classification` or `investigator_ae_classification`, the existing
`final_ae_classification` is cleared so the investigator must
reassess. This is the per-instance equivalent of the management
command's ``--update-copies`` mode.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .ae_final_classification import (
    AeFinalClassification,
    refresh_copies_from_sources,
)
from .ae_initial import AeInitial
from .ae_tmg import AeTmg


@receiver(
    post_save,
    sender=AeInitial,
    dispatch_uid="ae_initial_refresh_final_classification_on_post_save",
)
def ae_initial_refresh_final_classification_on_post_save(
    sender,  # noqa: ARG001
    instance,
    raw,
    **kwargs,  # noqa: ARG001
):
    if not raw:
        for obj in AeFinalClassification.objects.filter(ae_initial=instance).select_related(
            "ae_tmg"
        ):
            refresh_copies_from_sources(obj, instance, obj.ae_tmg)


@receiver(
    post_save,
    sender=AeTmg,
    dispatch_uid="ae_tmg_refresh_final_classification_on_post_save",
)
def ae_tmg_refresh_final_classification_on_post_save(
    sender,  # noqa: ARG001
    instance,
    raw,
    **kwargs,  # noqa: ARG001
):
    if not raw:
        qs = AeFinalClassification.objects.filter(
            ae_initial=instance.ae_initial,
        ).select_related("ae_initial")
        for obj in qs:
            refresh_copies_from_sources(obj, obj.ae_initial, instance)
