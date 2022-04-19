from edc_sites.single_site import SingleSite

fqdn = "effect.clinicedc.org"

all_sites = {
    "south_africa": (
        SingleSite(
            110,
            "capetown",
            title="UCT: Khayelitsha and Mitchell’s Plain (Cape Town)",
            country="south_africa",
            country_code="sa",
            domain=f"capetown.sa.{fqdn}",
        ),
        SingleSite(
            120,
            "baragwanath",
            title="Wits: Chris Hani Baragwanath (Soweto)",
            country="south_africa",
            country_code="sa",
            domain=f"baragwanath.sa.{fqdn}",
        ),
        SingleSite(
            130,
            "helen_joseph",
            title="Wits: Helen Joseph (Johannesburg)",
            country="south_africa",
            country_code="sa",
            domain=f"helen-joseph.sa.{fqdn}",
        ),
        SingleSite(
            140,
            "tshepong",
            title="Wits: Tshepong (Klerksdorp)",
            country="south_africa",
            country_code="sa",
            domain=f"tshepong.sa.{fqdn}",
        ),
        SingleSite(
            150,
            "king_edward",
            title="UKZN: King Edward VIII (Durban)",
            country="south_africa",
            country_code="sa",
            domain=f"king-edward.sa.{fqdn}",
        ),
        SingleSite(
            160,
            "harry_gwala",
            title="UKZN: Harry Gwala (Pietermaritzburg)",
            country="south_africa",
            country_code="sa",
            domain=f"harry-gwala.sa.{fqdn}",
        ),
        SingleSite(
            170,
            "livingstone",
            title="WSU: Livingstone (Gqeberha)",
            country="south_africa",
            country_code="sa",
            domain=f"livingstone.sa.{fqdn}",
        ),
        SingleSite(
            180,
            "dora_nginza",
            title="WSU: Dora Nginza (Gqeberha)",
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
