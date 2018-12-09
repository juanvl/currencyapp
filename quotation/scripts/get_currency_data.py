import requests, json, os

API_BASE_URL = os.environ.get("API_BASE_URL")
API_BASE_PORT = os.environ.get("API_BASE_PORT")
RESOURCE = "quotation/currencyquotations/create/"
HGBRASIL_API_URL = os.environ.get("HGBRASIL_API_URL")
HGBRASIL_API_KEY = os.environ.get("HGBRASIL_API_KEY")

try:
    url = "{}{}".format(HGBRASIL_API_URL, HGBRASIL_API_KEY)
    response = requests.get(url)
    api_data = response.text
except BaseException as error:
    print(str(error))

try:
    url = "{}:{}/{}".format(API_BASE_URL, API_BASE_PORT, RESOURCE)
    response = requests.post(url, data = {'api_data': api_data})
    if response.status_code == 200:
        print("Success retrieving currency api data")
    else:
        print("FAIL")
except BaseException as error:
    print(response.__dict__)
    print(str(error))
