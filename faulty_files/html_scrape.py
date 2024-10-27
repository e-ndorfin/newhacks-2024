import requests
from bs4 import BeautifulSoup
import pandas as pd
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('keys.env')
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set the API key directly in the openai module
openai.api_key = openai_api_key

# Keywords to search for in the web page content
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
    "environmental impact", "ecosystem damage", "wildlife displacement", "community impact"
]

# Set the state for filtering news URLs
state = 'AL'
df = pd.read_csv('USA_News_Sites.csv')
urls = df[df['state'] == state]['url']
print (list(urls))
list_urls = list(urls)[:1]


print(list_urls)

example = """Beyond Helene: Hurricane death toll tops 300 lives, with month left in season"""

# Loop through URLs and check for keywords
for url in list_urls:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html_content = response.text

        # Parse the HTML and get only the <body> content as HTML
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = str(soup.body).lower().replace("\n", "") if soup.body else ""  # Get full <body> HTML

        # Check for keywords in the body HTML only
        found_keywords = {keyword for keyword in keywords if keyword in body_content}

        # Extract and print all links within <body>
        links = soup.body.select('.link') if soup.body else []
        for link in links:
            print(link.get('href'))

        if found_keywords:
            print("Keywords found on the page:", found_keywords)

            # Split body content into smaller chunks (adjust size as needed)
            chunk_size = 15000  # Set chunk size (in characters)
            chunks = [body_content[i:i + chunk_size] for i in range(0, len(body_content), chunk_size)]
            total_chunks = len(chunks)

            # Process each chunk individually with GPT and print progress
            for i, chunk in enumerate(chunks, start=1):
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", 
                            "content": "You are a professional HTML programmer that is good at analytical activities and specializes in classifying article titles."}, 
                            {"role": "user",
                             "content": f"Identify any emergency-related information and associated links about recent natural disasters in the following HTML content. Focus on any current events and official reports. For example, if the content includes details similar to '{example}' but with same or different types of natural disaster, output the article title. ONLY OUTPUT ARTICLES THAT ARE ACTUALLY IN THE HTML CODE RELATING TO NATURAL DISASTERS AND EXTREME WEATHER, NOT NORMAL EMERGENCIES SUCH AS HUMAN CONFLICT OR WAR OR MURDER. {chunk}"}
                        ]
                    )
                    print(completion.choices[0].message['content'])
                    
                    # Print progress after GPT response
                    print(f"Processed chunk {i}/{total_chunks}")

                except openai.error.OpenAIError as e:
                    print(f"Error processing chunk {i}/{total_chunks}: {e}")
                    continue

        else:
            print("No keywords related to natural disasters found on the page.")

    except requests.exceptions.Timeout:
        print(f"Timeout occurred for {url}")

    except requests.exceptions.ConnectionError:
        print(f"Connection error for {url}")
