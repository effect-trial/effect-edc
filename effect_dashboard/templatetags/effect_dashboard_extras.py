from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from django import template
from django.conf import settings
from django.contrib.auth import get_permission_codename
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import INCOMPLETE, NO, PENDING, TBD, YES
from edc_dashboard.url_names import url_names
from edc_refusal.models import SubjectRefusal
from edc_subject_dashboard.view_utils import NextQuerystring

from effect_screening.eligibility import ScreeningEligibility

if TYPE_CHECKING:
    from effect_consent.models import SubjectConsent
    from effect_screening.models import SubjectScreening


register = template.Library()


@register.inclusion_tag(
    f"effect_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/" f"buttons/screening_button.html",
    takes_context=True,
)
def render_screening_button(context, subject_screening: SubjectScreening):
    nq = NextQuerystring(
        next_url_name="screening_listboard_url",
        reverse_kwargs=dict(
            screening_identifier=subject_screening.screening_identifier,
        ),
        extra_kwargs=dict(
            screening_identifier=subject_screening.screening_identifier,
            gender=subject_screening.gender,
            initials=subject_screening.initials,
            modified=subject_screening.modified,
        ),
    )
    url = f"{subject_screening.get_absolute_url()}?{nq.querystring}"
    fa_icon = "fa-eye" if subject_screening.consented else "fa-pencil"
    title = ("View" if subject_screening.consented else "Edit") + " subject's screening form"

    return dict(
        perms=context["perms"],
        screening_identifier=subject_screening.screening_identifier,
        eligible=subject_screening.eligible,
        href=url,
        fa_icon=fa_icon,
        title=title,
        NO=NO,
        PENDING=PENDING,
        TBD=TBD,
        YES=YES,
    )


@register.inclusion_tag(
    f"effect_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/" f"buttons/eligibility_button.html"
)
def render_eligibility_button(subject_screening: SubjectScreening):
    comment = []
    tooltip = None
    if not subject_screening.eligible and subject_screening.reasons_ineligible:
        comment = subject_screening.reasons_ineligible.split("|")
        comment = list(set(comment))
        comment.sort()
    eligibility = ScreeningEligibility(subject_screening, update_model=False)
    btn_color = "warning" if eligibility.display_label in [PENDING, INCOMPLETE] else "default"
    soup = BeautifulSoup(eligibility.display_label, features="html.parser")
    return dict(
        eligible=eligibility.is_eligible,
        eligible_final=eligibility.is_eligible,
        display_label=soup.get_text(),
        comment=comment,
        tooltip=tooltip,
        TBD=TBD,
        btn_color=btn_color,
    )


@register.inclusion_tag(
    f"effect_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/buttons/consent_button.html",
    takes_context=True,
)
def render_consent_button(context, subject_screening: SubjectScreening):
    nq = NextQuerystring(
        next_url_name="screening_listboard_url",
        reverse_kwargs=dict(
            screening_identifier=subject_screening.screening_identifier,
        ),
        extra_kwargs=dict(
            screening_identifier=subject_screening.screening_identifier,
            gender=subject_screening.gender,
            initials=subject_screening.initials,
            modified=subject_screening.modified,
        ),
    )
    model_cls = subject_screening.consent_definition.model_cls
    subject_consent = None
    try:
        subject_consent = model_cls.objects.get(
            screening_identifier=subject_screening.screening_identifier
        )
    except ObjectDoesNotExist:
        url = f"{model_cls().get_absolute_url()}?{nq.querystring}"
    else:
        url = f"{subject_consent.get_absolute_url()}?{nq.querystring}"
    fa_icon = "fa-pencil" if subject_consent else "fa-plus"
    title = "Edit consent" if subject_consent else "Consent subject to participate."
    add_codename = get_permission_codename("add", model_cls._meta)
    change_codename = get_permission_codename("change", model_cls._meta)
    codenames = [f"effect_consent.{add_codename}", f"effect_consent.{change_codename}"]
    disabled = "" if context["request"].user.has_perms(codenames) else "disabled"
    return dict(
        disabled=disabled,
        perms=context["perms"],
        screening_identifier=subject_screening.screening_identifier,
        href=url,
        consent_version=subject_screening.consent_definition.version,
        title=title,
        fa_icon=fa_icon,
    )


@register.inclusion_tag(
    f"effect_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/buttons/refusal_button.html",
    takes_context=True,
)
def render_refusal_button(context, subject_screening: SubjectScreening):
    nq = NextQuerystring(
        next_url_name="screening_listboard_url",
        reverse_kwargs=dict(
            screening_identifier=subject_screening.screening_identifier,
        ),
    )
    if subject_screening.consented:
        url = None
        title = "Not applicable. Subject has consented."
        fa_icon = "fa-eye-slash"
    else:
        try:
            subject_refusal = SubjectRefusal.objects.get(
                screening_identifier=subject_screening.screening_identifier
            )
        except ObjectDoesNotExist:
            url = f"{SubjectRefusal().get_absolute_url()}?{nq.querystring}"
            title = "Capture subject's primary reason for not joining."
            fa_icon = "fa-plus"
        else:
            url = f"{subject_refusal.get_absolute_url()}?{nq.querystring}"
            title = "Edit refusal"
            fa_icon = "fa-pencil"
    return dict(
        perms=context["perms"],
        screening_identifier=subject_screening.screening_identifier,
        href=url,
        title=title,
        fa_icon=fa_icon,
    )


@register.inclusion_tag(
    f"effect_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/buttons/dashboard_button.html"
)
def dashboard_button(subject_screening: SubjectScreening | SubjectConsent):
    subject_dashboard_url = url_names.get("subject_dashboard_url")
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=subject_screening.subject_identifier,
    )
