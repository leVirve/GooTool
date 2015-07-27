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


class Gooooogle():
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
        credential_path = os.path.join(credential_dir, self.CREDENTIALS_NAME)

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatability with Python 2.6
                credentials = tools.run(flow, store)
        return credentials

    def _new_service(self):
        """Creates a Google API service object.
        """
        httplib = self.credentials.authorize(httplib2.Http())
        return discovery.build(self.API_NAME, self.API_VERSION, http=httplib)
