from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class CurrencyRates(ApiBase):

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='getCurrencyRate')

    def get_all_generator(self, page_size=20):
        """
        Returns a generator which is more efficient memory-wise
        """
        return self._get_all_generator()


        
