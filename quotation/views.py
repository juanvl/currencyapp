from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from quotation.models import CurrencyQuotation
from quotation.serializers import CurrencyQuotationSerializer
from datetime import datetime, timedelta
import json


class CurrencyQuotationViewSet(ViewSet):

    def create(self, request):
        api_data = request.data.get("api_data", None)
        if not api_data:
            return Response({
                "detail": "api_data is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            api_data = json.loads(api_data)
            cq = CurrencyQuotation()
            cq.api_data = api_data
            cq.save()
        except BaseException as error:
            return Response({
                "detail": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(request.data, status=status.HTTP_200_OK,
                        content_type='application/json')

    def list(self, request):
        limit = request.GET.get('limit', None)
        if limit:
            limit = int(limit)
        try:
            all_cq = CurrencyQuotation.objects.all().order_by('-id')[:limit]
            serializer = CurrencyQuotationSerializer(all_cq, many=True)
        except BaseException as error:
            return Response({
                "detail": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.data, status=status.HTTP_200_OK,
                        content_type='application/json')

    def get_currency_variation(self, request):
        try:
            cq_now = CurrencyQuotation.objects.all().order_by('-id')[:1]
            cq_last_day = CurrencyQuotation.objects.filter(collected_at__lte=datetime.now()-timedelta(days=1)).order_by('-id')[:1]
            cq_last_week = CurrencyQuotation.objects.filter(collected_at__lte=datetime.now()-timedelta(days=7)).order_by('-id')[:1]
            cq_last_month = CurrencyQuotation.objects.filter(collected_at__lte=datetime.now()-timedelta(days=30)).order_by('-id')[:1]
            
            now_bitcoin_value = now_euro_value = now_dollar_value = 0
            last_day_bitcoin_value = last_day_euro_value = last_day_dollar_value = 0
            last_week_bitcoin_value = last_week_euro_value = last_week_dollar_value = 0
            last_month_bitcoin_value = last_month_euro_value = last_month_dollar_value = 0

            if cq_now:
                now_bitcoin_value = cq_now[0].api_data["results"]["currencies"]["BTC"]["buy"]
                now_euro_value = cq_now[0].api_data["results"]["currencies"]["EUR"]["buy"]
                now_dollar_value = cq_now[0].api_data["results"]["currencies"]["USD"]["buy"]

            if cq_last_day:
                last_day_bitcoin_value = cq_last_day[0].api_data["results"]["currencies"]["BTC"]["buy"]
                last_day_euro_value = cq_last_day[0].api_data["results"]["currencies"]["EUR"]["buy"]
                last_day_dollar_value = cq_last_day[0].api_data["results"]["currencies"]["USD"]["buy"]
            
            if cq_last_week:
                last_week_bitcoin_value = cq_last_week[0].api_data["results"]["currencies"]["BTC"]["buy"]
                last_week_euro_value = cq_last_week[0].api_data["results"]["currencies"]["EUR"]["buy"]
                last_week_dollar_value = cq_last_week[0].api_data["results"]["currencies"]["USD"]["buy"]
            
            if cq_last_month:
                last_month_bitcoin_value = cq_last_month[0].api_data["results"]["currencies"]["BTC"]["buy"]
                last_month_euro_value = cq_last_month[0].api_data["results"]["currencies"]["EUR"]["buy"]
                last_month_dollar_value = cq_last_month[0].api_data["results"]["currencies"]["USD"]["buy"]

            bitcoin_day_variation_percent = 0
            bitcoin_week_variation_percent = 0
            bitcoin_month_variation_percent = 0
            if now_bitcoin_value != 0:
                if last_day_bitcoin_value != 0:
                    bitcoin_day_variation_percent = (now_bitcoin_value - last_day_bitcoin_value) * 100 / last_day_bitcoin_value
                if last_week_bitcoin_value != 0:
                    bitcoin_week_variation_percent = (now_bitcoin_value - last_week_bitcoin_value) * 100 / last_week_bitcoin_value
                if last_month_bitcoin_value != 0:
                    bitcoin_month_variation_percent = (now_bitcoin_value - last_month_bitcoin_value) * 100 / last_month_bitcoin_value

            euro_day_variation_percent = 0
            euro_week_variation_percent = 0
            euro_month_variation_percent = 0
            if now_bitcoin_value != 0:
                if last_day_euro_value != 0:
                    euro_day_variation_percent = (now_euro_value - last_day_euro_value) * 100 / last_day_euro_value
                if last_week_euro_value != 0:
                    euro_week_variation_percent = (now_euro_value - last_week_euro_value) * 100 / last_week_euro_value
                if last_month_euro_value != 0:
                    euro_month_variation_percent = (now_euro_value - last_month_euro_value) * 100 / last_month_euro_value
            
            dollar_day_variation_percent = 0
            dollar_week_variation_percent = 0
            dollar_month_variation_percent = 0
            if now_bitcoin_value != 0:
                if last_day_dollar_value != 0:
                    dollar_day_variation_percent = (now_dollar_value - last_day_dollar_value) * 100 / last_day_dollar_value
                if last_week_dollar_value != 0:
                    dollar_week_variation_percent = (now_dollar_value - last_week_dollar_value) * 100 / last_week_dollar_value
                if last_month_dollar_value != 0:
                    dollar_month_variation_percent = (now_dollar_value - last_month_dollar_value) * 100 / last_month_dollar_value
            
            currency_variation_percent = {
                "bitcoin": {
                    "day_variation": bitcoin_day_variation_percent,
                    "week_variation": bitcoin_week_variation_percent,
                    "month_variation": bitcoin_month_variation_percent,
                },
                "euro": {
                    "day_variation": euro_day_variation_percent,
                    "week_variation": euro_week_variation_percent,
                    "month_variation": euro_month_variation_percent,
                },
                "dollar": {
                    "day_variation": dollar_day_variation_percent,
                    "week_variation": dollar_week_variation_percent,
                    "month_variation": dollar_month_variation_percent,
                }
            }
            
        except BaseException as error:
            return Response({
                "detail": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(currency_variation_percent, status=status.HTTP_200_OK,
                        content_type='application/json')

