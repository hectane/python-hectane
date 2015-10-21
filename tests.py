from __future__ import absolute_import

from pyhectane import Connection


class TestConnection:
    """
    Run some simple tests to ensure the Connection class works correctly.
    """

    def setUp(self):
        """
        Create a connection to the server.
        """
        self._connection = Connection()
