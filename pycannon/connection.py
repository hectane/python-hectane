from requests import Session


class Connection:
    """
    Connection to go-cannon for sending emails.
    """

    def __init__(self, tls=False, host='localhost', port=8025, username=None,
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

    def version(self):
        """
        Obtain the current version of go-cannon.
        """
        return self._session.get("{}/version".format(self._url)).json()['version']
