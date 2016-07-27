from oauth2client import tools

from gootool.google_service import GoogleClient

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class YoutubeMe(GoogleClient):

    SCOPES = 'https://www.googleapis.com/auth/youtube.readonly'
    CLIENT_SECRET_FILE = 'client_secret_youtube.json'
    CREDENTIALS_NAME = 'youtube-credential.json'
    APPLICATION_NAME = 'Youtube got playlists'
    API_NAME = "youtube"
    API_VERSION = 'v3'

    def __init__(self):
        super(YoutubeMe, self).__init__()

    def get_playlists(self):
        """Retrieve at most 50 playlists at once
        """
        playlists_response = self.service.playlists().list(
            mine=True, part="snippet", maxResults=50
        ).execute()

        f = open('youtube-lists.txt', 'w', encoding='utf8')
        for playlist in playlists_response["items"]:
            f.write('===== 清單 %s =====\n' % playlist['snippet']['title'])

            playlistitems_list_request = self.service.playlistItems().list(
                playlistId=playlist["id"], part="snippet", maxResults=50
            )
            while playlistitems_list_request:
                playlistitems_list_response = playlistitems_list_request.execute()
                for playlist_item in playlistitems_list_response["items"]:
                    title = playlist_item["snippet"]["title"]
                    video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                    f.write("%s (%s)\n" % (title, video_id))

                playlistitems_list_request = self.service.playlistItems(). \
                    list_next(
                        playlistitems_list_request,
                        playlistitems_list_response
                    )
