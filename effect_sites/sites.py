from edc_sites.single_site import SingleSite

fqdn = "effect.clinicedc.org"

all_sites = {
    "south_africa": (
        SingleSite(
            110,
            "capetown",
            title="Khayelitsha and Mitchell’s Plain",
            country="south_africa",
            country_code="sa",
            domain=f"capetown.sa.{fqdn}",
        ),
        SingleSite(
            120,
            "baragwanath",
            title="Chris Hani Baragwanath Hospital",
            country="south_africa",
            country_code="sa",
            domain=f"baragwanath.sa.{fqdn}",
        ),
        SingleSite(
            130,
            "helen_joseph",
            title="Helen Joseph Hospital",
            country="south_africa",
            country_code="sa",
            domain=f"helen-joseph.sa.{fqdn}",
        ),
        SingleSite(
            140,
            "klerksdorp",
            title="Klerksdorp/Tshepong Hospital",
            country="south_africa",
            country_code="sa",
            domain=f"klerksdorp.sa.{fqdn}",
        ),
        SingleSite(
            150,
            "king_edward",
            title="King Edward VIII Hospital",
            country="south_africa",
            country_code="sa",
            domain=f"king-edward.sa.{fqdn}",
        ),
        SingleSite(
            160,
            "edendale",
            title="Edendale Hospital",
            country="south_africa",
            country_code="sa",
            domain=f"edendale.sa.{fqdn}",
        ),
        SingleSite(
            170,
            "livingstone",
            title="Livingstone Hospital",
            country="south_africa",
            country_code="sa",
            domain=f"livingstone.sa.{fqdn}",
        ),
        SingleSite(
            180,
            "dora_nginza",
            title="Dora Nginza Hospital",
            country="south_africa",
            country_code="sa",
            domain=f"dora-nginza.sa.{fqdn}",
        ),
    ),
    "tanzania": (
        SingleSite(
            200,
            "amana",
            title="Amana Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"amana.tz.{fqdn}",
        ),
        SingleSite(
            210,
            "temeke",
            title="Temeke Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"temeke.tz.{fqdn}",
        ),
        SingleSite(
            220,
            "mwananyamala",
            title="Mwananyamala Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"mwananyamala.tz.{fqdn}",
        ),
    ),
}
