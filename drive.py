from apiclient import errors
from oauth2client import tools

import google_service

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class DriveMan(google_service.Gooooogle):

    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'client_secret.json'
    CREDENTIALS_NAME = 'drive-credential.json'
    API_NAME = "drive"
    API_VERSION = 'v2'
    APPLICATION_NAME = 'Drive download'

    def __init__(self):
        super(DriveMan, self).__init__()

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
