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


if __name__ == '__main__':
    drive = DriveMan()

    # get meta data by id
    meta = drive.get_metadata('XXXXXXXXXXXXXXXXXXXXX')
    print(meta)

    # download file by id
    resp = drive.download('XXXXXXXXXXXXXXXXXXXXX')
    print(resp)
