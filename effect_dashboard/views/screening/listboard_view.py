import re

from django.db.models import Q
from edc_constants.constants import ABNORMAL
from edc_dashboard.view_mixins import (
    EdcViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
)
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin
from edc_screening.model_wrappers import SubjectScreeningModelWrapper

from .filters import ListboardViewFilters


class ListboardView(
    EdcViewMixin,
    NavbarViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
    BaseListboardView,
):

    listboard_template = "screening_listboard_template"
    listboard_url = "screening_listboard_url"
    listboard_panel_style = "info"
    listboard_fa_icon = "fa-user-plus"
    listboard_view_filters = ListboardViewFilters()
    listboard_model = "effect_screening.subjectscreening"
    listboard_view_permission_codename = "edc_dashboard.view_screening_listboard"

    alternate_search_attr = "screening_identifier"

    model_wrapper_cls = SubjectScreeningModelWrapper
    navbar_selected_item = "screened_subject"
    ordering = "-report_datetime"
    paginate_by = 10
    search_form_url = "screening_listboard_url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            subject_screening_add_url=self.get_subject_screening_add_url(),
            ABNORMAL=ABNORMAL,
        )
        return context

    def get_subject_screening_add_url(self):
        return self.listboard_model_cls().get_absolute_url()

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get("screening_identifier"):
            options.update({"screening_identifier": kwargs.get("screening_identifier")})
        return options

    def extra_search_options(self, search_term):
        q_objects = []
        if re.match(r"^[A-Z\-]+$", search_term):
            q_objects.append(Q(initials__exact=search_term.upper()))
            q_objects.append(
                Q(screening_identifier__icontains=search_term.replace("-", "").upper())
            )
        return q_objects
