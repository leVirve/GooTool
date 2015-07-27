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

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive download'


def get_credentials():
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
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
    return credentials


def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs.
    """
    credentials = get_credentials()
    httplib = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=httplib)

    item = print_file_metadata(service, 'FILE ID')
    with open(item['title'], 'wb') as f:
        f.write(download_file(service, item))


def print_file_metadata(service, file_id):
    """Print a file's metadata.

    Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
    """
    try:
        file = service.files().get(fileId=file_id).execute()

        print('Title: %s' % file['title'])
        return file
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def download_file(service, drive_file):
    """Download a file's content.

    Args:
    service: Drive API service instance.
    drive_file: Drive File instance.

    Returns:
    File's content if successful, None otherwise.
    """
    download_url = drive_file.get('downloadUrl')
    if download_url:
        print('Go', download_url)
        resp, content = service._http.request(download_url)
        if resp.status == 200:
            print('Status: %s' % resp)
            return content
        else:
            print('An error occurred: %s' % resp)
            return None
    else:
        # The file doesn't have any content stored on Drive.
        return None

if __name__ == '__main__':
    main()
