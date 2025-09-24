from multisite import SiteID

from .defaults import *  # noqa

style = color_style()  # noqa: F405

sys.stdout.write(style.MIGRATE_HEADING(f"Settings file {__file__}\n"))  # noqa: F405

# SA Sites
# SITE_ID = SiteID(default=110)  # Capetown (Khayelitsha & Mitchell's Plain)
# SITE_ID = SiteID(default=160)  # Harry Gwala (Pietermaritzburg)
# SITE_ID = SiteID(default=150)  # King Edward VII
# SITE_ID = SiteID(default=120)  # Baragwanath
# SITE_ID = SiteID(default=130)  # Helen Joseph
SITE_ID = SiteID(default=140)  # Tshepong (Klerksdorp)
# SITE_ID = SiteID(default=170)  # Livingstone (Gqeberha)
# SITE_ID = SiteID(default=180)  # Dora Nginza (Gqeberha)

# TZ Sites
# SITE_ID = SiteID(default=200)  # Amana
# SITE_ID = SiteID(default=220)  # Mwananyamala
# SITE_ID = SiteID(default=210)  # Temeke

EDC_SITES_UAT_DOMAIN = False
DEBUG = True
ALLOWED_HOSTS = [
    "localhost",
    "mnazi-moja.tz.meta3.clinicedc.org",
    "mbagala.tz.meta3.clinicedc.org",
    "mwananyamala.tz.meta3.clinicedc.org",
    "hindu-mandal.tz.meta3.clinicedc.org",
    "temeke.tz.meta3.clinicedc.org",
    "amana.tz.meta3.clinicedc.org",
]

SECURE_SSL_REDIRECT = False
AUTO_CREATE_KEYS = False
EDC_MODEL_ADMIN_CSS_THEME = "edc_indigo"
