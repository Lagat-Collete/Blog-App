from urllib import response
import requests
from .models import Quotes


api ='http://quotes.stormconsultancy.co.uk/random.json'

def get_quotes():
    response = requests.get(f'{api}')
    quote = response.json()
    quotes = Quotes(quote.get('author'), quote.get('quote'))
    return quotes