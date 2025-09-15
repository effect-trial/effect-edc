import sys

from multisite import SiteID

from .defaults import *  # noqa

sys.stdout.write(f"Settings file {__file__}\n")

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
AUTO_CREATE_KEYS = False

EDC_MODEL_ADMIN_CSS_THEME = "edc_indigo"

# DJANGO_REVISION_IGNORE_WORKING_DIR = True
