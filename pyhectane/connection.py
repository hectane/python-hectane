from base64 import b64encode
from mimetypes import guess_type
from os.path import basename

from requests import Session
from six import string_types


class Connection:
    """
    Connection to Hectane for sending emails.
    """

    def __init__(self, host='localhost', port=8025, tls=False, username=None,
                 password=None):
        """
        Provide the security information and credentials necessary to make
        connections to the Hectane API.
        """
        self._session = Session()
        if username and password:
            self._session.auth = (username, password)
        self._url = '{}://{}:{}/v1'.format(
            'https' if tls else 'http',
            host, port,
        )

    def _process_attachments(self, attachments):
        """
        Create attachments suitable for delivery to Hectane from the provided
        list of attachments.

        Each attachment may be either a local filename, a file object, or a
        dict describing the content (in the same format as Hectane). Note that
        if the filename cannot be determined, it will be set to "untitled".
        """
        for a in attachments:
            if isinstance(a, dict):
                yield a
            else:
                if isinstance(a, string_types):
                    a = open(a, 'rb')
                filename = basename(getattr(a, 'name', 'untitled'))
                yield {
                    "filename": filename,
                    "content_type": guess_type(filename)[0] or 'application/octet-stream',
                    "content": b64encode(a.read()).decode(),
                    "encoded": True,
                }

    def raw(self, from_, to, body):
        """
        Send a raw MIME message.
        """
        if isinstance(to, string_types):
            raise TypeError('"to" parameter must be enumerable')
        return self._session.post('{}/raw'.format(self._url), json={
            'from': from_,
            'to': to,
            'body': body,
        }).json()

    def send(self, from_, to, subject, text='', html='', cc=[], bcc=[],
             attachments=[]):
        """
        Send an email.
        """
        if isinstance(to, string_types):
            raise TypeError('"to" parameter must be enumerable')
        if text == '' and html == '':
            raise ValueError('"text" and "html" must not both be empty')
        return self._session.post('{}/send'.format(self._url), json={
            'from': from_,
            'to': to,
            'cc': cc,
            'bcc': bcc,
            'subject': subject,
            'text': text,
            'html': html,
            'attachments': list(self._process_attachments(attachments)),
        }).json()

    def status(self):
        """
        Retrieve status information.
        """
        return self._session.get('{}/status'.format(self._url)).json()

    def version(self):
        """
        Retrieve the application version.
        """
        return self._session.get('{}/version'.format(self._url)).json()
