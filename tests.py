from __future__ import absolute_import

from six.moves import BaseHTTPServer

from .pyhectane import Connection


class SimpleHttpServer(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    Extremely simple HTTP server that captures request information and stores
    it for later retrieval.
    """


class TestConnection:
    """
    Run some simple tests to ensure the Connection class works correctly.
    """

    def setUp(self):
        """
        Create a connection to the server.
        """
        self._connection = Connection()
