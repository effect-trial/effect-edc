from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(
    post_save, weak=False, dispatch_uid="calculate_headache_duration_timedelta_on_post_save"
)
def calculate_headache_duration_timedelta_on_post_save(
    sender, instance, raw, created, using, **kwargs
):
    if not raw and not kwargs.get("update_fields"):
        try:
            instance.update_calculated_headache_duration()
        except AttributeError as e:
            if "update_calculated_headache_duration" not in str(e):
                raise
