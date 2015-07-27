import httplib2
import os

import oauth2client
from apiclient import discovery, errors
from oauth2client import client, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class DriveMan():

    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Drive download'

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
        credential_path = os.path.join(credential_dir, 'drive-credential.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                DriveMan.CLIENT_SECRET_FILE, DriveMan.SCOPES)
            flow.user_agent = DriveMan.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatability with Python 2.6
                credentials = tools.run(flow, store)
        return credentials

    def _new_service(self):
        """Creates a Google Drive API service object.
        """
        httplib = self.credentials.authorize(httplib2.Http())
        return discovery.build('drive', 'v2', http=httplib)

    def get_metadata(self, file_id):
        try:
            return self.service.files().get(fileId=file_id).execute()
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def download(self, file_id):
        """Download a file's content.

        Args:
        file_id: Drive File id.

        Returns:
        Response data from Google Drive if successful, None otherwise.
        """
        drive_file = self.get_metadata(file_id)
        download_url = drive_file.get('downloadUrl')

        if download_url:
            resp, content = self.service._http.request(download_url)
            if resp.status == 200:
                with open(drive_file['originalFilename'], 'wb') as f:
                    f.write(content)
                return resp
            else:
                print('An error occurred: %s' % resp)
                return None
        else:
            # The file doesn't have any content stored on Drive.
            return None

if __name__ == '__main__':
    drive = DriveMan()

    # get meta data by id
    meta = drive.get_metadata('XXXXXXXXXXXXXXXXXXXXX')
    print(meta)

    # download file by id
    resp = drive.download('XXXXXXXXXXXXXXXXXXXXX')
    print(resp)
