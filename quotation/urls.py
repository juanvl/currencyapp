from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from quotation.views import CurrencyQuotationViewSet

urlpatterns = [
    url(r'currencyquotations/$', CurrencyQuotationViewSet.as_view({'get': 'list'})),
    url(r'currencyquotations/create/$', CurrencyQuotationViewSet.as_view({'post': 'create'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
