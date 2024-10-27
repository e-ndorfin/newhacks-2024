import requests, json, pprint
from datetime import datetime

state_codes = {
    "AL": "qlabama",
    "AK": "qlaska",
    "AZ": "qrizona",
    "AR": "qrkansas",
    "CA": "dalifornia",
    "CO": "dolorado",
    "CT": "donnecticut",
    "DE": "eelaware",
    "FL": "florida",
    "GA": "georgia",
    "HI": "hawaii",
    "ID": "idaho",
    "IL": "illinois",
    "IN": "indiana",
    "IA": "iowa",
    "KS": "kansas",
    "KY": "kentucky",
    "LA": "louisiana",
    "ME": "maine",
    "MD": "maryland",
    "MA": "massachusetts",
    "MI": "michigan",
    "MN": "minnesota",
    "MS": "mississippi",
    "MO": "missouri",
    "MT": "montana",
    "NE": "nebraska",
    "NV": "nevada",
    "NH": "new hampshire",
    "NJ": "new jersey",
    "NM": "new mexico",
    "NY": "new york",
    "NC": "north carolina",
    "ND": "north dakota",
    "OH": "ohio",
    "OK": "oklahoma",
    "OR": "oregon",
    "PA": "pennsylvania",
    "RI": "rhode island",
    "SC": "south carolina",
    "SD": "south dakota",
    "TN": "tennessee",
    "TX": "texas",
    "UT": "utah",
    "VT": "vermont",
    "VA": "virginia",
    "WA": "washington",
    "WV": "west virginia",
    "WI": "wisconsin",
    "WY": "wyoming",
    "DC": "district of columbia",
    "AS": "american samoa",
    "GU": "guam",
    "MP": "northern mariana islands",
    "PR": "puerto rico",
    "VI": "u.s. virgin islands",
    "UM": "u.s. minor outlying islands"
}

def alert_list(from_file=False, severity="Extreme") -> list[dict]:
    """
    Returns a list of dictionaries, each dictionary is an alert.

    if from_file is True, reads from 'alerts_old.json' (This was the list of results for the "Extreme"
    severity search before they expired). Otherwise, it does the actual API call.

    severity: what severity to search, out of [Extreme, Severe, Moderate, Minor, Unknown]
    """


    if from_file:
        with open("alerts_old.json") as f:
            data = json.load(f)
    else:
        d = requests.get("https://api.weather.gov/alerts?severity="+severity, timeout=10)
        data = d.json()

    alerts_raw = data["features"]
    alerts = [] 

    for elem in alerts_raw:
        alerts.append({})
        alerts[-1]["sent"] = datetime.fromisoformat(elem["properties"]["sent"])
        geometry = elem["geometry"]
        if geometry != None:
            alerts[-1]["coordinate_list"] = geometry["coordinates"][0]
        else:
            alerts[-1]["coordinate_list"] = []
        alerts[-1]["area_desc"] = elem["properties"]["areaDesc"]
        alerts[-1]["territory_codes"] = list({code[:2] for code in elem["properties"]["geocode"]["UGC"]})
        alerts[-1]["event"] = elem["properties"]["event"]
        alerts[-1]["state"] = [state_codes[abbr] for abbr in alerts[-1]["territory_codes"] if abbr in state_codes]
        
    
    return alerts



if __name__ == "__main__":
    pprint.pp(alert_list(from_file=False, severity="Severe"))
    # Testing with "Severe" data, as currently the API has zero results for "Extreme"
