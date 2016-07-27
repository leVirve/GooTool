import os

import httplib2
import oauth2client
from apiclient import discovery


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args('')
except ImportError:
    flags = None


class GoogleClient():

    SCOPES = 'https://www.googleapis.com/auth/'
    CLIENT_SECRET_FILE = 'client_secret.json'
    CREDENTIAL_FOLDER = './.credentials'
    CREDENTIAL_FILENAME = 'credential.json'
    API_NAME = 'google-client-default'
    API_VERSION = 'v2'
    APPLICATION_NAME = 'google-client'

    def __init__(self):
        self.credentials = self.get_credentials()
        self.service = self.new_service()

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        store = self._get_credential_store()
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = self._gen_auth_flow()
            credentials = oauth2client.tools.run_flow(flow, store, flags)
        return credentials

    def new_service(self):
        """Creates a Google API service object.
        """
        http_auth = self.credentials.authorize(httplib2.Http())
        return discovery.build(self.API_NAME, self.API_VERSION, http=http_auth)

    def _gen_auth_flow(self):
        flow = oauth2client.client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
        flow.user_agent = self.APPLICATION_NAME
        return flow

    def _get_credential_store(self):
        path = self._get_credential_path()
        return oauth2client.file.Storage(path)

    def _get_credential_path(self):
        credential_dir = self._ensure_dir()
        return os.path.join(credential_dir, self.CREDENTIAL_FILENAME)

    def _ensure_dir(self):
        os.makedirs(self.CREDENTIAL_FOLDER, exist_ok=True)
        return self.CREDENTIAL_FOLDER