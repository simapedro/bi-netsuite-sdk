import zeep
import logging
from collections import OrderedDict

from netsuitesdk.internal.client import NetSuiteClient
from netsuitesdk.internal.utils import PaginatedSearch
from typing import List

logger = logging.getLogger(__name__)


# TODO: introduce arg and return types
class ApiBase:
    def __init__(self, ns_client: NetSuiteClient, type_name):
        self.ns_client = ns_client
        self.type_name = type_name

    def search(self, attribute, value, operator):
        """
        Search Record
        :param attribute: name of the field, eg. entityId
        :param value: value of the field, eg. Amazon
        :param operator: search matching operator, eg., 'contains', 'is', 'anyOf'
        :return:
        """
        records = self.ns_client.basic_stringfield_search(
            type_name=self.type_name,
            attribute=attribute,
            value=value,
            operator=operator
        )

        return records

    def search_currency_rates(self, base_currency, transaction_currency, effective_date):
        """
        Search for Currency Rate records in NetSuite.

        :param base_currency: Base currency (e.g., 'USD')
        :param transaction_currency: Transaction currency (e.g., 'EUR')
        :param effective_date: Effective date for the rate (e.g., '2024-02-01')
        :return: Currency Rate records
        """
        search_criteria = {
            "basic": {
                "baseCurrency": [{"operator": "anyOf", "searchValue": base_currency}],
                "transactionCurrency": [{"operator": "anyOf", "searchValue": transaction_currency}],
                "effectiveDate": [{"operator": "onOrBefore", "searchValue": effective_date}]
            }
        }

        try:
            records = self.ns_client.search(record_type="CurrencyRate", search_criteria=search_criteria)
            return records
        except Exception as e:
            print(f"Error fetching currency rates: {e}")
            return None

    def get_all(self):
        generated_records = self.get_all_generator()
        all_records = []
        for records in generated_records:
            all_records.extend(records)
        return all_records

    def count(self):
        ps = PaginatedSearch(client=self.ns_client, type_name=self.type_name, pageSize=10, perform_search=True)
        return ps.total_records

    def get_all_generator(self, page_size=20):
        """
        Returns a generator which is more efficient memory-wise
        """
        return self.create_paginated_search(page_size=page_size)

    def get(self, internalId=None, externalId=None) -> OrderedDict:
        return self._get(internalId=internalId, externalId=externalId)

    def get_ref(self, internalId=None, externalId=None) -> OrderedDict:
        return self._serialize(self.ns_client.RecordRef(type=self.type_name.lower(),
                                                        internalId=internalId, externalId=externalId))

    def post(self, data) -> OrderedDict:
        raise NotImplementedError('post method not implemented')

    def _serialize(self, record) -> OrderedDict:
        """
        record: single record
        Returns a dict
        """
        return zeep.helpers.serialize_object(record)

    def _serialize_array(self, records) -> List[OrderedDict]:
        """
        records: a list of records
        Returns an array of dicts
        """
        return zeep.helpers.serialize_object(records)

    @staticmethod
    def _paginated_search_to_generator(paginated_search):
        if paginated_search.num_records == 0:
            return

        num_pages = paginated_search.total_pages
        logger.debug('total pages = %d, records in page = %d', paginated_search.total_pages, paginated_search.num_records)
        logger.debug(f'current page index {paginated_search.page_index}')
        logger.debug('going to page %d', 0)
        
        for p in range(1, num_pages + 1):
            logger.debug('going to page %d', p)
            paginated_search.goto_page(p)
            logger.debug(f'current page index {paginated_search.page_index}')
            yield paginated_search.records

    @staticmethod
    def _paginated_search_generator(paginated_search: PaginatedSearch):
        if paginated_search.num_records == 0:
            return

        num_pages = paginated_search.total_pages
        logger.debug('total pages = %d, records in page = %d', paginated_search.total_pages, paginated_search.num_records)
        logger.debug(f'current page index {paginated_search.page_index}')
        logger.debug('going to page %d', 0)

        for p in range(1, num_pages + 1):
            logger.debug('going to page %d', p)
            paginated_search.goto_page(p)
            logger.debug(f'current page index {paginated_search.page_index}')
            yield paginated_search.records

    def create_paginated_search(self, page_size):
        ps = PaginatedSearch(client=self.ns_client, type_name=self.type_name, pageSize=page_size)
        return self._paginated_search_generator(paginated_search=ps)

    def _search_all_generator(self, page_size):
        ps = PaginatedSearch(client=self.ns_client, type_name=self.type_name, pageSize=page_size)
        return self._paginated_search_to_generator(paginated_search=ps)

    def _get_all(self) -> List[OrderedDict]:
        records = self.ns_client.getAll(recordType=self.type_name)
        return self._serialize_array(records)
    
    def _get_all_generator(self):
        res = self._get_all()
        for r in res:
            yield r

    def _get(self, internalId=None, externalId=None) -> OrderedDict:
        record = self.ns_client.get(recordType=self.type_name, internalId=internalId, externalId=externalId)
        return record

    def build_simple_fields(self, fields, source, target):
        for field in fields:
            if field in source:
                target[field] = source[field]

    def build_record_ref_fields(self, fields, source, target):
        for field in fields:
            if field in source:
                target[field] = self.ns_client.RecordRef(**(source[field]))
