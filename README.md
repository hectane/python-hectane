## pyhectane

[![License](http://img.shields.io/badge/license-MIT-yellow.svg)](http://opensource.org/licenses/MIT)
[![PyPI Version](http://img.shields.io/pypi/v/pyhectane.svg)](https://pypi.python.org/pypi/pyhectane)
[![PyPI Downloads](http://img.shields.io/pypi/dm/pyhectane.svg)](https://pypi.python.org/pypi/pyhectane)

A Python module for sending emails with [Hectane](https://github.com/hectane/hectane).

### Installation

Installing pyhectane is as simple as:

    pip install pyhectane

### Usage

Accessing the Hectane API with pyhectane centers around the `Connection` object. The example below demonstrates the process of creating an instance and using it to send a simple email:

    import pyhectane

    c = pyhectane.Connection()

    c.send(
        from_='me@me.com',
        to=['you@you.com'],
        subject="Email Subject",
        text="Email body.",
        attachments=[
            'somefile.zip',
            'otherfile.tar.gz',
        ],
    )

### Django Backend

For projects using the [Django framework](https://www.djangoproject.com/), an email backend for Hectane is available. To use the backend, add the following line to `settings.py`:

    EMAIL_BACKEND = 'pyhectane.django.HectaneBackend'

The following settings are also recognized:

- `HECTANE_HOST`
- `HECTANE_PORT`
- `HECTANE_TLS`
- `HECTANE_USERNAME`
- `HECTANE_PASSWORD`
