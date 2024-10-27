import openai
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from maps import return_map

# Load environment variables
load_dotenv('keys.env')


client = MongoClient('mongodb+srv://zacharytang24:zDTAalcoWz5Ock7Z@pulse.2x4ku.mongodb.net/')

db = client['pulse_db']

collection = db['users']

companies = collection.find()

client.close()

# Set up OpenAI and Mailgun API keys from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")
mailgun_api_key = os.getenv("MAILGUN_API_KEY")
mailgun_domain = os.getenv("MAILGUN_DOMAIN")

def generate_disaster_email(company_name, industry, location, disaster_name):
    # Define the prompt for the ChatGPT API
    prompt = f"""
    Write a professional email to {company_name}, a company in the {industry} industry located in {location}. 
    Inform them about a recent natural disaster, {disaster_name}, affecting the area. Include details on the type of disaster, 
    its severity, and potential impacts on the {industry} industry and safety precautions for their employees. Tailor the message to provide helpful insights 
    on what they might need to know or do. Output this in HTML, using <p> elements FOR THE WHOLE TEXT and <strong> ONLY WHEN NECESSARY. Keep the email short and succinct less than 1000 characters. Make the signature "Regards, Pulse Team."
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are an expert in writing professional business communication."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        
        email_content = response['choices'][0]['message']['content']
        return email_content

    except Exception as e:
        print("An error occurred:", e)
        return None

import requests
from PIL import Image
from io import BytesIO

# Mailgun and Google API keys
mailgun_api_key = "YOUR_MAILGUN_API_KEY"
mailgun_domain = "YOUR_MAILGUN_DOMAIN"
google_api_key = "YOUR_GOOGLE_MAPS_API_KEY"

def generate_map_image(state_abbreviation):
    # Geocode the state to get the center coordinates
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={state_abbreviation},USA&key={google_api_key}"
    geocode_response = requests.get(geocode_url)
    if geocode_response.status_code == 200:
        geocode_data = geocode_response.json()
        if geocode_data["results"]:
            location = geocode_data["results"][0]["geometry"]["location"]
            latitude, longitude = location["lat"], location["lng"]

            # Generate static map image
            zoom = 7
            size = "600x600"
            static_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size={size}&key={google_api_key}"
            map_response = requests.get(static_map_url)
            if map_response.status_code == 200:
                return BytesIO(map_response.content)
            else:
                print(f"Failed to retrieve the map image: {map_response.text}")
        else:
            print("Failed to find the center coordinates for the state.")
    else:
        print(f"Geocoding API request failed: {geocode_response.text}")
    return None

def send_email_with_mailgun(subject, recipient_email, email_content, attachment=None):
    from_email = f"Mailgun Service <mailgun@{mailgun_domain}>"
    url = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"

    data = {
        "from": from_email,
        "to": recipient_email,
        "subject": subject,
        "html": email_content
    }

    files = [("attachment", ("map_image.png", attachment, "image/png"))] if attachment else None

    try:
        response = requests.post(url, auth=("api", mailgun_api_key), data=data, files=files)
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Status code: {response.status_code}")
            print(response.json())

    except Exception as e:
        print("Failed to send email with Mailgun:", e)




# Example usage
for company in companies: 
    company_info = {
        "company_name": company['name'],
        "industry": company['company_type'],
        "location": company['state'],
        "email": company['email'],
    }

    generated_email_content = generate_disaster_email(
        company_info['company_name'], 
        company_info['industry'], 
        company_info['location'], 
        'Hurricane Helene'
    )
    
    map_image = generate_map_image(company['state'])

    if generated_email_content and map_image:
        send_email_with_mailgun(
            subject="Important Notice: Natural Disaster Alert",
            recipient_email=company_info['email'],
            email_content=generated_email_content, attachment=map_image
        )
