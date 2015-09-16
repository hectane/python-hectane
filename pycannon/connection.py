from base64 import encodestring
from mimetypes import guess_type
from os.path import basename

from requests import Session
from six import string_types


class Connection:
    """
    Connection to go-cannon for sending emails.
    """

    def __init__(self, host='localhost', port=8025, tls=False, username=None,
                 password=None):
        """
        Provide the security information and credentials necessary to make
        connections to the go-cannon API.
        """

        # Create the session that will store the authentication information
        self._session = Session()

        # If credentials were provided, use them
        if username and password:
            self._session.auth = (username, password)

        # Build the URL that will be used for accessing the API
        self._url = '{}://{}:{}/v1'.format(
            'https' if tls else 'http',
            host, port,
        )

    def _process_attachments(self, attachments):
        """
        Convert a list of strings and file objects to a list of attachment
        objects with the appropriate attributes.
        """
        for a in attachments:

            # If a string was provided, treat it as a filename
            if isinstance(a, string_types):
                a = open(a, 'rb')

            # Read and encode the contents and determine the filename
            content = encodestring(a.read())
            filename = basename(getattr(a, 'name', 'untitled'))

            # Yield the content of the attachment
            yield {
                "filename": filename,
                "content_type": guess_type(filename)[0] or 'application/octet-stream',
                "content": content,
                "encoded": True,
            }

    def send(self, from_, to, subject, text='', html='', cc=[], bcc=[],
             attachments=[]):
        """
        Send an email using go-cannon.
        """

        # Ensure "to" is a list
        if isinstance(to, string_types):
            raise TypeError('"to" parameter must be enumerable')

        # Ensure either "text" or "html" was provided
        if text == '' and html == '':
            raise ValueError('"text" and "html" must not both be empty')

        return self._session.post("{}/send".format(self._url), json={
            'from': from_,
            'to': to,
            'cc': cc,
            'bcc': bcc,
            'subject': subject,
            'text': text,
            'html': html,
            'attachments': list(self._process_attachments(attachments)),
        }).json()

    def version(self):
        """
        Obtain the current version of go-cannon.
        """
        return self._session.get("{}/version".format(self._url)).json()
