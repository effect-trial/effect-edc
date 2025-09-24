from multisite import SiteID

from .defaults import *  # noqa

style = color_style()  # noqa: F405

sys.stdout.write(style.MIGRATE_HEADING(f"Settings file {__file__}\n"))  # noqa: F405

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
AUTO_CREATE_KEYS = False

EDC_MODEL_ADMIN_CSS_THEME = "edc_indigo"

# DJANGO_REVISION_IGNORE_WORKING_DIR = True
