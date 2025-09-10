from django.db import models


class MissedDosesManager(models.Manager):
    def get_by_natural_key(
        self,
        day_missed,
        missed_reason,
        subject_identifier,
        visit_schedule_name,
        schedule_name,
        visit_code,
    ):
        return self.get(
            day_missed=day_missed,
            missed_reason=missed_reason,
            subject_visit__subject_identifier=subject_identifier,
            subject_visit__visit_schedule_name=visit_schedule_name,
            subject_visit__schedule_name=schedule_name,
            subject_visit__visit_code=visit_code,
        )
