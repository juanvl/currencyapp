from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from quotation.models import CurrencyQuotation
from quotation.serializers import CurrencyQuotationSerializer
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
        try:
            all_cq = CurrencyQuotation.objects.all()
            serializer = CurrencyQuotationSerializer(all_cq, many=True)
        except BaseException as error:
            return Response({
                "detail": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.data, status=status.HTTP_200_OK,
                        content_type='application/json')

