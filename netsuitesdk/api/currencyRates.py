from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class CurrencyRates(ApiBase):

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='CurrencyRate')

    def get_all(self):
        return self._get_all()

