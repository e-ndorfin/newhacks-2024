import requests
from bs4 import BeautifulSoup
import pandas as pd
from openai import OpenAI


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

#url = "http://www.reflector.com/"

state = 'alabama'
df = pd.read_csv('USA_News_Sites.csv')
urls = df[df['state'] == state]['url']
list_urls = list(urls)
# urls = df.iloc[:,0]

print(list_urls)

for url in list_urls: 
    try:
        response = requests.get(url,timeout=10) 
        response.raise_for_status() 
        html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text().lower()
        found_keywords = {keyword for keyword in keywords if keyword in text}

        links = soup.select('.link')
        for link in links:
            print(link.get('href')) 

        if found_keywords:
            print(found_keywords)
            source = response.text

            client = OpenAI()

            completion = client.chat.completions.create(
            model="gpt-4o",
            messages={"role": "system", 
                    "content": "Find the headers related to natural disasters and their respective links in the following html newspaper sources.",
                    "role": "user",
                    "content": source})

            print(completion.choices[0].message)
        else:
            pass

    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.ConnectionError:
        pass

