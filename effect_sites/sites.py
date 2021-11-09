from edc_sites.single_site import SingleSite

fqdn = "effect.clinicedc.org"

all_sites = {
    "south_africa": (
        SingleSite(
            110,
            "capetown",
            title="Khayelitsha district hospital and Mitchell’s Plain hospital",
            country="south_africa",
            country_code="sa",
            domain=f"capetown.sa.{fqdn}",
        ),
        SingleSite(
            120,
            "baragwanath",
            title="Chris Hani Baragwanath academic hospital, Soweto",
            country="south_africa",
            country_code="sa",
            domain=f"baragwanath.sa.{fqdn}",
        ),
        SingleSite(
            130,
            "helen_joseph",
            title="Helen Joseph hospital, Johannesburg",
            country="south_africa",
            country_code="sa",
            domain=f"helen-joseph.sa.{fqdn}",
        ),
        SingleSite(
            140,
            "klerksdorp",
            title="Klerksdorp/Tshepong hospital",
            country="south_africa",
            country_code="sa",
            domain=f"klerksdorp.sa.{fqdn}",
        ),
        SingleSite(
            150,
            "king_edward",
            title="King Edward VIII hospital, Durban",
            country="south_africa",
            country_code="sa",
            domain=f"king-edward.sa.{fqdn}",
        ),
        SingleSite(
            160,
            "edendale",
            title="Edendale hospital, Pietermaritzburg",
            country="south_africa",
            country_code="sa",
            domain=f"edendale.sa.{fqdn}",
        ),
        SingleSite(
            170,
            "livingstone",
            title="Livingstone hospital, Port Elizabeth",
            country="south_africa",
            country_code="sa",
            domain=f"livingstone.sa.{fqdn}",
        ),
        SingleSite(
            180,
            "dora_nginza",
            title="Dora Nginza hospital, Port Elizabeth",
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
