from rest_framework import serializers
from quotation.models import CurrencyQuotation
import pytz


class CurrencyQuotationSerializer(serializers.ModelSerializer):
    api_data = serializers.SerializerMethodField()
    collected_at = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyQuotation
        fields = ("api_data", "collected_at")

    @staticmethod
    def get_api_data(cq):
        cq_return = {
            "quotation_real": {
                "bitcoin": cq.api_data["results"]["currencies"]["BTC"],
                "euro": cq.api_data["results"]["currencies"]["EUR"],
                "dollar": cq.api_data["results"]["currencies"]["USD"],
            }
        }

        return cq_return
    
    @staticmethod
    def get_collected_at(cq):
        time_zone = pytz.timezone('America/Sao_Paulo')
        date_time = time_zone.localize(cq.collected_at)
        formatedDate = date_time.strftime("%H:%M")
        return formatedDate
