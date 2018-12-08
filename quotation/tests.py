from django.test import TestCase
from django.conf import settings
from rest_framework import status
from quotation.models import CurrencyQuotation
import json, requests


class CurrencyQuotationViewSetTestCase(TestCase):

    def setUp(self):
        self.api_data_sample = {
            "by": "default",
            "valid_key": True,
            "results": {
                "currencies": {
                    "source": "BRL",
                    "USD": {
                        "name": "Dollar",
                        "buy": 3.8902,
                        "sell": None,
                        "variation": 0.39
                    },
                    "EUR": {
                        "name": "Euro",
                        "buy": 4.4468,
                        "sell": None,
                        "variation": 0.77
                    },
                    "GBP": {
                        "name": "Pound Sterling",
                        "buy": 4.9755,
                        "sell": None,
                        "variation": 0.355
                    },
                    "ARS": {
                        "name": "Argentine Peso",
                        "buy": 0.1047,
                        "sell": None,
                        "variation": 1.749
                    },
                    "BTC": {
                        "name": "Bitcoin",
                        "buy": 13679.835,
                        "sell": 13679.835,
                        "variation": -4.81
                    }
                },
                "stocks": {
                    "IBOVESPA": {
                        "name": "BM&F BOVESPA",
                        "location": "Sao Paulo, Brazil",
                        "points": 88115.07,
                        "variation": -0.82
                    },
                    "NASDAQ": {
                        "name": "NASDAQ Stock Market",
                        "location": "New York City, United States",
                        "variation": -3.05
                    },
                    "CAC": {
                        "name": "CAC 40",
                        "location": "Paris, French",
                        "variation": 0.68
                    },
                    "NIKKEI": {
                        "name": "Nikkei 225",
                        "location": "Tokyo, Japan",
                        "variation": 0.82
                    }
                },
                "available_sources": [
                    "BRL"
                ],
                "bitcoin": {
                    "blockchain_info": {
                        "name": "Blockchain.info",
                        "format": [
                            "USD",
                            "en_US"
                        ],
                        "last": 3314.08,
                        "buy": 3314.08,
                        "sell": 3314.08,
                        "variation": -4.906
                    },
                    "coinbase": {
                        "name": "Coinbase",
                        "format": [
                            "USD",
                            "en_US"
                        ],
                        "last": 3270.7,
                        "variation": -4.838
                    },
                    "bitstamp": {
                        "name": "BitStamp",
                        "format": [
                            "USD",
                            "en_US"
                        ],
                        "last": 3275.4,
                        "buy": 3275.25,
                        "sell": 3272.24,
                        "variation": -4.67
                    },
                    "foxbit": {
                        "name": "FoxBit",
                        "format": [
                            "BRL",
                            "pt_BR"
                        ],
                        "last": 12851.01,
                        "variation": -5.783
                    },
                    "mercadobitcoin": {
                        "name": "Mercado Bitcoin",
                        "format": [
                            "BRL",
                            "pt_BR"
                        ],
                        "last": 13159.67,
                        "buy": 13041.3,
                        "sell": 13157.675,
                        "variation": -2.881
                    },
                    "omnitrade": {
                        "name": "OmniTrade",
                        "format": [
                            "BRL",
                            "pt_BR"
                        ],
                        "last": 13300.2,
                        "buy": 13300.1,
                        "sell": 13650,
                        "variation": 0.001
                    },
                    "xdex": {
                        "name": "XDEX",
                        "format": [
                            "BRL",
                            "pt_BR"
                        ],
                        "last": 13000,
                        "variation": -4.288
                    }
                }
            },
            "execution_time": 0,
            "from_cache": True
        }
        self.cq = CurrencyQuotation()
        self.cq.api_data = self.api_data_sample
        self.cq.save()

    def test_create(self):
        url = "https://api.hgbrasil.com/finance/quotations?format=json&key={}".format(settings.HG_BRASIL_API_KEY)
        try:
            response = requests.get(url)
            api_data = response.text
        except BaseException as error:
            return str(error)

        url = "/quotation/currencyquotations/create/"

        response = self.client.post(
            url,
            data=json.dumps({ 'api_data': api_data }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content_type, 'application/json')

    def test_create_invalid(self):
        url = "/quotation/currencyquotations/create/"

        response = self.client.post(
            url,
            data=json.dumps({ 'test': 'test' }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list(self):
        url = "/quotation/currencyquotations/"

        response = self.client.get(
            url,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content_type, 'application/json')

    def test_list_empty(self):
        CurrencyQuotation.objects.all().delete()
        url = "/quotation/currencyquotations/"

        response = self.client.get(
            url,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content_type, 'application/json')
    
    