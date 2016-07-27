from gootool.google_service import GoogleClient


class YoutubeMe(GoogleClient):

    SCOPES = 'https://www.googleapis.com/auth/youtube.readonly'
    CREDENTIAL_FILENAME = 'youtube-credential.json'
    APPLICATION_NAME = 'Youtube got playlists'
    API_NAME = "youtube"
    API_VERSION = 'v3'

    def __init__(self, output='youtube-lists.txt'):
        super(YoutubeMe, self).__init__()
        self.output = output

    def get_playlists(self):
        """Retrieve at most 50 playlists at once
        """
        f = open(self.output, 'w', encoding='utf8')

        playlists = self._get_playlists()

        for playlist in playlists["items"]:
            f.write('===== 清單 %s =====\n' % playlist['snippet']['title'])

            request = self._gen_items_request(playlist['id'])

            while request:
                response = request.execute()
                for playlist_item in response['items']:
                    title = playlist_item['snippet']['title']
                    video_id = playlist_item['snippet']['resourceId']['videoId']
                    f.write('%s (%s)\n' % (title, video_id))

                request = self.service.playlistItems(). \
                    list_next(request, response)

    def _get_playlists(self):
        playlists = self.service.playlists().list(
            mine=True, part="snippet", maxResults=50
        ).execute()
        return playlists

    def _gen_items_request(self, playlist_id):
        request = self.service.playlistItems().list(
            playlistId=playlist_id, part="snippet", maxResults=50
        )
        return request
