from copy import copy

from django.conf import settings
from edc_adverse_event.navbars import ae_navbar_item, tmg_navbar_item
from edc_data_manager.navbar_item import dm_navbar_item
from edc_lab_dashboard.navbars import navbar as lab_navbar
from edc_navbar import Navbar, site_navbars
from edc_review_dashboard.navbars import navbar as review_navbar

from effect_dashboard.navbars import navbar as dashboard_navbar

navbar = Navbar(name=settings.APP_NAME)

navbar_item = copy([item for item in lab_navbar.navbar_items if item.name == "specimens"][0])
navbar_item.active = False
navbar_item.label = "Specimens"
navbar.register(navbar_item)

navbar.register(
    [item for item in dashboard_navbar.navbar_items if item.name == "screened_subject"][0]
)

navbar.register(
    [item for item in dashboard_navbar.navbar_items if item.name == "consented_subject"][0]
)

for item in review_navbar.navbar_items:
    navbar.register(item)

navbar.register(tmg_navbar_item)
navbar.register(ae_navbar_item)
navbar.register(dm_navbar_item)


site_navbars.register(navbar)
