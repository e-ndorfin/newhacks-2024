import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import openai
from html_scrape import scrape_main_page
from dotenv import load_dotenv
import os

load_dotenv('keys.env')
openai_api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
client = OpenAI(api_key=openai_api_key)
a = scrape_main_page()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", 
    "content": "Go through the list and check if each item in the list is talking about a natural disaster that is happening or not. Man-made disasters such as war or politics should not be a yes. Respond in a list in python form which only shows a yes or no answer for each item."},
    {"role": "user",
    "content": str(a) } 
  ]
)
print(completion)

import re
ret = []
for word in completion['choices'][0]['message']['content'].split(','):
    ret.append(re.sub(r'[^a-zA-Z]', '', word))

filtered_values = [value for yn, value in zip(ret, a) if yn == "yes"]
print(filtered_values)




