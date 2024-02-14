from typing import Any

from edc_randomization.utils import (
    get_assignment_description_for_subject,
    get_assignment_for_subject,
)
from edc_subject_dashboard.views import SubjectDashboardView


class DashboardView(SubjectDashboardView):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        kwargs.update(
            assignment=get_assignment_for_subject(
                subject_identifier=self.kwargs.get("subject_identifier"),
                randomizer_name="default",
            ),
            assignment_description=get_assignment_description_for_subject(
                subject_identifier=self.kwargs.get("subject_identifier"),
                randomizer_name="default",
            ),
        )
        return super().get_context_data(**kwargs)
