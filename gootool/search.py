import logging
from gootool.google_service import GoogleClient

logger = logging.getLogger('gootool')


class Search(GoogleClient):

    APPLICATION_NAME = 'Search for interests'
    API_NAME = 'customsearch'
    API_VERSION = 'v1'

    def __init__(self, developer_key, cx, output='search-result.json'):
        super().__init__(oauth=False, developer_key=developer_key)
        self.cx = cx

    def query(self, keyword, search_type=None, page=3):
        result = []
        request = self._gen_search_request(keyword, search_type)
        for _ in range(page):
            response = request.execute()
            request = self._gen_search_next_request(response, keyword, search_type)
            result.append(response)
        return result

    def _gen_search_request(self, keyword, search_type):
        request = self.service.cse().list(
            cx=self.cx,
            q=keyword, searchType=search_type
        )
        return request

    def _gen_search_next_request(self, response, keyword, search_type):
        request = self.service.cse().list(
            cx=self.cx,
            q=keyword, searchType=search_type,
            start=response['queries']['nextPage'][0]['startIndex'])
        return request
