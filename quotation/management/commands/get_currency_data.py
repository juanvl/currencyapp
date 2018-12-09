from django.core.management.base import BaseCommand
from django.conf import settings
import requests, json


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = "https://api.hgbrasil.com/finance/quotations?format=json&key={}".format(settings.HG_BRASIL_API_KEY)
        try:
            response = requests.get(url)
            api_data = response.text
        except BaseException as error:
            return str(error)
        
        url = "http://localhost:8000/quotation/currencyquotations/create/"
        try:
            response = requests.post(url, data = {'api_data': api_data})
            if response.status_code == 200:
                print("Success retrieving currency api data")
            else:
                print("FAIL")
        except BaseException as error:
            print(response.__dict__)
            return str(error)
