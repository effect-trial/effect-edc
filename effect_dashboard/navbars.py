from edc_adverse_event.navbars import ae_navbar_item, tmg_navbar_item
from edc_data_manager.navbar_item import dm_navbar_item
from edc_navbar import Navbar, NavbarItem, site_navbars
from edc_review_dashboard.navbars import navbar_item as review_navbar_item

no_url_namespace = False  # True if settings.APP_NAME == "effect_dashboard" else False

navbar = Navbar(name="effect_dashboard")

navbar.append_item(
    NavbarItem(
        name="screened_subject",
        title="Screening",
        label="Screening",
        fa_icon="fa-solid fa-user-plus",
        codename="edc_screening.view_screening_listboard",
        url_name="screening_listboard_url",
        no_url_namespace=no_url_namespace,
    )
)

navbar.append_item(
    NavbarItem(
        name="consented_subject",
        title="Subjects",
        label="Subjects",
        fa_icon="fa-solid fa-user-circle",
        codename="edc_subject_dashboard.view_subject_listboard",
        url_name="subject_listboard_url",
        no_url_namespace=no_url_namespace,
    )
)

navbar.append_item(review_navbar_item)
navbar.append_item(tmg_navbar_item)
navbar.append_item(ae_navbar_item)
navbar.append_item(dm_navbar_item)

site_navbars.register(navbar)
