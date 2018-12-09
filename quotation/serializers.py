from rest_framework import serializers
from quotation.models import CurrencyQuotation


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
        formatedDate = cq.collected_at.strftime("%H:%M")
        return formatedDate
