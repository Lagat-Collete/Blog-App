from urllib import response
import requests,json
from .models import Quotes


BASE_URL ='http://quotes.stormconsultancy.co.uk/random.json'

def get_quotes():
    response = requests.get(f"{BASE_URL}")
    if response.status_code ==200:
      quote = response.json()
      return quote