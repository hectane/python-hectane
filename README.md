## pycannon

[![License](http://img.shields.io/badge/license-MIT-red.svg)](http://opensource.org/licenses/MIT)

A Python module for sending emails with [go-cannon](https://github.com/nathan-osman/go-cannon).

### Usage

Accessing the go-cannon API with pycannon centers around the creation of a `Connection` object. The example below demonstrates the process of sending a simple email:

    import pycannon

    c = pycannon.Connection()

    c.send(
        'me@me.com',
        ['you@you.com'],
        "Email Subject",
        "Plain text body.",
    )
