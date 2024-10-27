import requests, json, pprint
from datetime import datetime

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
    
    return alerts



if __name__ == "__main__":
    pprint.pp(alert_list(from_file=False, severity="Severe"))
    # Testing with "Severe" data, as currently the API has zero results for "Extreme"