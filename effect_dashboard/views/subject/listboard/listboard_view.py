from django.db.models import Min, Q
from edc_dashboard.view_mixins import EdcViewMixin
from edc_listboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_listboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin


class ListboardView(
    EdcViewMixin,
    NavbarViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
    BaseListboardView,
):
    listboard_template = "subject_listboard_template"
    listboard_url = "subject_listboard_url"
    listboard_panel_style = "success"
    listboard_fa_icon = "far fa-user-circle"
    listboard_model = "effect_consent.subjectconsent"
    listboard_view_permission_codename = "edc_subject_dashboard.view_subject_listboard"
    navbar_selected_item = "consented_subject"
    search_form_url = "subject_listboard_url"
    search_fields = [
        "initials__exact",
        "subject_identifier",
        "screening_identifier",
        "first_name__exact",
        "last_name__exact",
        "identity__exact",
    ]

    def get_updated_queryset(self, queryset):
        """Only return records with first consent for each subject."""
        sub_qs = queryset.values("subject_identifier").annotate(
            min_consent_datetime=Min("consent_datetime")
        )
        queryset = queryset.filter(
            subject_identifier__in=sub_qs.values("subject_identifier"),
            consent_datetime__in=sub_qs.values("min_consent_datetime"),
        )
        return queryset

    def get_queryset_filter_options(self, request, *args, **kwargs) -> tuple[Q, dict]:
        q_object, options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get("subject_identifier"):
            options.update({"subject_identifier": kwargs.get("subject_identifier")})
        return q_object, options
