import httplib2
import os

import oauth2client
from apiclient import discovery
from oauth2client import client, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class YoutubeMe():

    SCOPES = 'https://www.googleapis.com/auth/youtube.readonly'
    CLIENT_SECRETS_FILE = 'client_secret.json'
    API_NAME = "youtube"
    API_VERSION = 'v3'

    def __init__(self):
        self.credentials = self._get_credentials()
        self.service = self._new_service()

    def _get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_dir = os.path.join('./', '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'youtube-credential.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                YoutubeMe.CLIENT_SECRETS_FILE, YoutubeMe.SCOPES)
            flow.user_agent = YoutubeMe.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatability with Python 2.6
                credentials = tools.run(flow, store)
        return credentials

    def _new_service(self):
        """Creates a Google Drive API service object.
        """
        httplib = self.credentials.authorize(httplib2.Http())
        return discovery.build(
            YoutubeMe.API_NAME,
            YoutubeMe.API_VERSION,
            http=httplib)

    def get_playlists(self):
        """Retrieve at most 50 playlists at once
        """
        playlists_response = self.service.playlists().list(
            mine=True,
            part="snippet",
            maxResults=50
        ).execute()

        f = open('youtube-lists.txt', 'w', encoding='utf8')
        for playlist in playlists_response["items"]:
            uploads_list_id = playlist["id"]

            f.write('========= 清單 %s ==========\n' % playlist['snippet']['title'])

            playlistitems_list_request = self.service.playlistItems().list(
                playlistId=uploads_list_id,
                part="snippet",
                maxResults=50
            )

            while playlistitems_list_request:
                playlistitems_list_response = playlistitems_list_request.execute()

                # Print information about each video.
                for playlist_item in playlistitems_list_response["items"]:
                    title = playlist_item["snippet"]["title"]
                    video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                    f.write("%s (%s)\n" % (title, video_id))

                playlistitems_list_request = self.service.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)

if __name__ == '__main__':
    youtube = YoutubeMe()
    youtube.get_playlists()
