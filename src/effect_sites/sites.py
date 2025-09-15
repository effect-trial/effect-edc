from edc_sites import site_sites
from edc_sites.single_site import SingleSite

__all__ = ["all_sites"]

suffix = "effect.clinicedc.org"
sa_language_codes = ["en", "af", "st", "sw", "tn", "xh", "zu"]

tz_language_codes = ["sw", "en", "mas"]

vi_language_codes = ["vi", "en"]

all_sites = [
    SingleSite(
        110,
        "capetown",
        title="UCT: Khayelitsha and Mitchell's Plain (Cape Town)",
        country="south_africa",
        country_code="sa",
        language_codes=sa_language_codes,
        domain=f"capetown.sa.{suffix}",
    ),
    SingleSite(
        120,
        "baragwanath",
        title="Wits: Chris Hani Baragwanath (Soweto)",
        country="south_africa",
        country_code="sa",
        language_codes=sa_language_codes,
        domain=f"baragwanath.sa.{suffix}",
    ),
    SingleSite(
        130,
        "helen_joseph",
        title="Wits: Helen Joseph (Johannesburg)",
        country="south_africa",
        country_code="sa",
        language_codes=sa_language_codes,
        domain=f"helen-joseph.sa.{suffix}",
    ),
    SingleSite(
        140,
        "tshepong",
        title="Wits: Tshepong (Klerksdorp)",
        country="south_africa",
        country_code="sa",
        language_codes=sa_language_codes,
        domain=f"tshepong.sa.{suffix}",
    ),
    SingleSite(
        150,
        "king_edward",
        title="UKZN: King Edward VIII (Durban)",
        country="south_africa",
        country_code="sa",
        language_codes=sa_language_codes,
        domain=f"king-edward.sa.{suffix}",
    ),
    SingleSite(
        160,
        "harry_gwala",
        title="UKZN: Harry Gwala (Pietermaritzburg)",
        country="south_africa",
        country_code="sa",
        language_codes=sa_language_codes,
        domain=f"harry-gwala.sa.{suffix}",
    ),
    SingleSite(
        170,
        "livingstone",
        title="WSU: Livingstone (Gqeberha)",
        country="south_africa",
        country_code="sa",
        language_codes=sa_language_codes,
        domain=f"livingstone.sa.{suffix}",
    ),
    SingleSite(
        180,
        "dora_nginza",
        title="WSU: Dora Nginza (Gqeberha)",
        country="south_africa",
        country_code="sa",
        language_codes=sa_language_codes,
        domain=f"dora-nginza.sa.{suffix}",
    ),
    SingleSite(
        200,
        "amana",
        title="Amana Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"amana.tz.{suffix}",
    ),
    SingleSite(
        210,
        "temeke",
        title="Temeke Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"temeke.tz.{suffix}",
    ),
    SingleSite(
        220,
        "mwananyamala",
        title="Mwananyamala Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"mwananyamala.tz.{suffix}",
    ),
]

site_sites.register(*all_sites)
