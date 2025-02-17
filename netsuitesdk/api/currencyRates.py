from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class CurrencyRates(ApiBase):

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='CurrencyRate')

    def search_currency_rates(self, base_currency='USD', transaction_currency='EUR', effective_date='2/17/2025'):
        """
        Returns a generator which is more efficient memory-wise
        """
        return self._search_currency_rates()
    