import openai
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('keys.env')

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

def send_email_with_mailgun(subject, recipient_email, email_content):
    from_email = f"Mailgun Service <mailgun@{mailgun_domain}>"
    url = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"

    data = {
        "from": from_email,
        "to": recipient_email,
        "subject": subject,
        "html": email_content
    }

    try:
        response = requests.post(url, auth=("api", mailgun_api_key), data=data)
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Status code: {response.status_code}")
            print(response.json())

    except Exception as e:
        print("Failed to send email with Mailgun:", e)

# Example usage
company_info = {
    "company_name": "Telus",
    "industry": "Telecommunications",
    "location": "Ontario",
    "email": "patrickjedrzejko@gmail.com",
    "disaster_name": "Flood"
}

generated_email_content = generate_disaster_email(
    company_info['company_name'], 
    company_info['industry'], 
    company_info['location'], 
    company_info['disaster_name']
)

if generated_email_content:
    send_email_with_mailgun(
        subject="Important Notice: Natural Disaster Alert for Ontario Region",
        recipient_email=company_info['email'],
        email_content=generated_email_content
    )
