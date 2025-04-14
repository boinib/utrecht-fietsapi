import requests
import pandas as pd

API_URL = "https://stallingsnet.nl/api/1/parkingcount/utrecht"

def get_parking_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    df = pd.DataFrame(response.json())

    coords = {
        "House Modernes": [52.09330172273189, 5.115784922159138],
        "House Modernes Laag": [52.0930, 5.1165],
        "House Modernes Hoog": [52.0936, 5.1140],

        "Keizerstraat": [52.09451050496849, 5.12492493942988],
        "Keizerstraat Laag": [52.0940, 5.1242],
        "Keizerstraat Hoog": [52.0950, 5.1251],

        "Knoop": [52.08747041057327, 5.109601439351618],
        "Knoop Laag": [52.0879, 5.1097],
        "Knoop Hoog": [52.0881, 5.1094],

        "Laag Catharijne": [52.09182379928891, 5.112747784926727],
        "Laag Catharijne Laag": [52.0912, 5.1130],
        "Laag Catharijne Hoog": [52.0921, 5.1123],

        "Neude": [52.09302799555306, 5.118177468265716],
        "Neude Hoog": [52.0926, 5.1185],
        "Neude Laag": [52.0924, 5.1180],

        "Pop Up Domplein": [52.0907818347391, 5.121926516147517],
        "Pop Up Jacobskerkhof": [52.094948406933234, 5.115310768265824],
        "Pop Up Janskerkhof": [52.0931967707523, 5.1220677449835295],
        "Pop Up Mariaplaats": [52.08993836859217, 5.116711037578421],
        "Pop Up Neude": [52.093246120130445, 5.119277375670654],
        "Pop Up Vredenburg": [52.093131620434825, 5.113901508208987],

        "Stadhuis": [52.09241080891099, 5.12023102532754],
        "Stadhuis Hoog": [52.0920, 5.1203],
        "Stadhuis Laag": [52.0926, 5.1200],

        "Stationsplein": [52.09151078435688, 5.110561361519456],
        "Stationsplein Hoog": [52.0910, 5.1109],
        "Stationsplein Laag": [52.0912, 5.1104],

        "UB Plein": [52.0948923417452, 5.1256675537060525],
        "UB Plein Hoog": [52.0943, 5.1258],
        "UB Plein Laag": [52.0950, 5.1253],

        "Vredenburg": [52.092954457310704, 5.114044671892185],
        "Vredenburg Hoog": [52.0920, 5.1143],
        "Vredenburg Laag": [52.0925, 5.1139],

        "Zadelstraat": [52.09006094915963, 5.118434754773205],
        "Zadelstraat Hoog": [52.0903, 5.1186],
        "Zadelstraat Laag": [52.0900, 5.1182],

        "Jaarbeursplein": [52.08919754654059, 5.1076501984188845],

        "P+R Westraven": [52.05740891227885, 5.105377768263674],
        "Pop Up Stationsplein": [52.090803746087076, 5.111336931491021],
        "Pop Up Smakkelaarsveld": [52.09224725081396, 5.110307854697101],
        "Pop Up Moreelsepark": [52.088245637200544, 5.115225687294562],
        "Pop Up Catharijnesingel": [52.086832559604666, 5.117550792865112],
        "Pop Up Springweg": [52.08721693616238, 5.1202194198497635],
    }

    def lookup_coords(name):
        if name in coords:
            return coords[name]
        for key in coords:
            if key.lower() in name.lower():
                return coords[key]
        return [None, None]

    df[["lat", "lon"]] = df["facilityName"].apply(lambda name: pd.Series(lookup_coords(name)))
    return df
