from requests import Session


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

    def send(self, from_, to, subject, text, html='', cc=[], bcc=[]):
        """
        Send an email using go-cannon.
        """
        return self._session.post("{}/send".format(self._url), json={
            'from': from_,
            'to': to,
            'cc': cc,
            'bcc': bcc,
            'subject': subject,
            'text': text,
            'html': html,
        }).json()

    def version(self):
        """
        Obtain the current version of go-cannon.
        """
        return self._session.get("{}/version".format(self._url)).json()
