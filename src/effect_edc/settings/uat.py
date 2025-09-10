from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = True
AUTO_CREATE_KEYS = False
LIVE_SYSTEM = False

EDC_MODEL_ADMIN_CSS_THEME = "edc_purple"
