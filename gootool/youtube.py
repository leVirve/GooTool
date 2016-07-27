import logging
from gootool.google_service import GoogleClient

logger = logging.getLogger('gootool')


class YoutubeMe(GoogleClient):

    SCOPES = 'https://www.googleapis.com/auth/youtube.readonly'
    CREDENTIAL_FILENAME = 'youtube-credential.json'
    APPLICATION_NAME = 'Youtube got playlists'
    API_NAME = "youtube"
    API_VERSION = 'v3'

    def __init__(self, credential=None, client_secret=None, output='youtube-lists.txt'):
        super(YoutubeMe, self).__init__(credential, client_secret)
        self.output = output

    def get_playlists(self):
        """Retrieve at most 50 playlists at once
        """
        request = self._gen_playlists_request()
        playlists = request.execute()
        logger.debug(playlists)

        results = [
            {
                'title': playlist['snippet']['title'],
                'videos': self.get_playlist(playlist['id'])
            } for playlist in playlists['items']
        ]
        return results

    def get_playlist(self, playlist_id):
        videos = []
        request = self._gen_items_request(playlist_id)
        while request:
            response = request.execute()
            logger.debug(response)
            videos += [
                {
                    'title': item['snippet']['title'],
                    'id': item['snippet']['resourceId']['videoId']
                } for item in response['items']
            ]
            request = self._gen_items_next_request(request, response)
        return videos

    def _gen_playlists_request(self):
        request = self.service.playlists().list(
            mine=True, part="snippet", maxResults=50
        )
        return request

    def _gen_items_request(self, playlist_id):
        request = self.service.playlistItems().list(
            playlistId=playlist_id, part="snippet", maxResults=50)
        return request

    def _gen_items_next_request(self, request, response):
        request = self.service.playlistItems().list_next(request, response)
        return request
