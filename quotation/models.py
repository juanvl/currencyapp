from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class CurrencyQuotation(models.Model):
    api_data = JSONField(null=True, blank=True)
    collected_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.collected_at)