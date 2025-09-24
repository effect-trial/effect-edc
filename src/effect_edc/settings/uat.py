from multisite import SiteID

from .defaults import *  # noqa

style = color_style()  # noqa: F405

sys.stdout.write(style.MIGRATE_HEADING(f"Settings file {__file__}\n"))  # noqa: F405

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = True
AUTO_CREATE_KEYS = False
LIVE_SYSTEM = False

EDC_MODEL_ADMIN_CSS_THEME = "edc_purple"

SILENCED_SYSTEM_CHECKS = ["edc_visit_schedule.E009", "sites.E101"]
