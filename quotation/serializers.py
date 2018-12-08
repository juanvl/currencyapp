from rest_framework import serializers
from quotation.models import CurrencyQuotation


class CurrencyQuotationSerializer(serializers.ModelSerializer):
    api_data = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyQuotation
        fields = ("api_data", "collected_at")

    @staticmethod
    def get_api_data(cq):
        cq_api_data = cq.api_data

        cq_return = {
            "quotation_real": {
                "bitcoin": cq_api_data["results"]["currencies"]["BTC"],
                "euro": cq_api_data["results"]["currencies"]["EUR"],
                "dollar": cq_api_data["results"]["currencies"]["USD"],
            }
        }

        return cq_return
