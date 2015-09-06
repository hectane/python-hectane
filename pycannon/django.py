from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from .connection import Connection


class GoCannonBackend(BaseEmailBackend):
    """
    Django email backend for go-cannon.
    """

    def __init__(self, **kwargs):
        """
        Initialize the connection to go-cannon.
        """
        super(GoCannonBackend, self).__init__(**kwargs)
        self._connection = Connection(
            host=getattr(settings, 'GO_CANNON_HOST', 'localhost'),
            port=getattr(settings, 'GO_CANNON_PORT', 8025),
            tls=getattr(settings, 'GO_CANNON_TLS', False),
            username=getattr(settings, 'GO_CANNON_USERNAME', None),
            password=getattr(settings, 'GO_CANNON_PASSWORD', None),
        )

    def send_messages(self, emails):
        """
        Attempt to send the specified emails.
        """
        num_sent = 0
        for e in emails:
            r = self._connection.send(
                from_=e.from_email,
                to=e.to,
                subject=e.subject,
                text=e.body,
                html=None,
                cc=e.cc,
                bcc=e.bcc,
            )
            if 'error' not in r:
                num_sent += 1
        return num_sent
