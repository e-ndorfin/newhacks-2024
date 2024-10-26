import requests
from bs4 import BeautifulSoup
import pandas as pd

keywords = [
    "earthquake", "tremor", "seismic", "aftershock",
    "hurricane", "cyclone", "typhoon", "storm", "tropical storm", "wind speeds",
    "flood", "flash flood", "inundation", "water levels", "river overflow",
    "landslide", "mudslide", "debris flow", "soil erosion",
    "volcano", "eruption", "lava", "ash cloud", "pyroclastic flow",
    "tsunami", "wave surge", "ocean swell", "sea level rise",
    "wildfire", "forest fire", "bushfire", "fire containment", "fire spread",
    "drought", "heatwave", "dry spell", "water shortage",
    "storm surge", "tidal surge", "coastal erosion",
    "evacuation", "emergency response", "rescue", "disaster relief", "humanitarian aid",
    "casualties", "fatalities", "injuries", "damage assessment", "property damage",
    "recovery efforts", "disaster management", "risk assessment", "crisis response",
    "climate change", "extreme weather", "natural hazards", "preparedness", "response team",
    "power outage", "infrastructure damage", "communication breakdown", "relief shelters",
    "contamination", "disease outbreak", "pandemic risk", "air quality", "water quality",
    "environmental impact", "ecosystem damage", "wildlife displacement", "community impact"]

df = pd.read_csv('USA_News_Sites.csv')
urls = df.iloc[:,0]

print(urls)
url = "http://www.reflector.com/"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")
text = soup.get_text().lower()
found_keywords = {keyword for keyword in keywords if keyword in text}

links = soup.select('.link')
for link in links:
    print(link.get('href')) 

if found_keywords:
    print("Keywords found on the page:", found_keywords)
else:
    print("No keywords related to natural disasters found on the page.")


