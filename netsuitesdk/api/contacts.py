from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class Contacts(ApiBase):

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Contact')

    def get_all(self):
        return self._get_all()

    def get_all_generator(self, page_size=20):
        """
        Returns a generator which is more efficient memory-wise
        """
        return self._get_all_generator()


        
