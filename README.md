## pycannon

[![License](http://img.shields.io/badge/license-MIT-yellow.svg)](http://opensource.org/licenses/MIT)
[![PyPI Version](http://img.shields.io/pypi/v/pycannon.svg)](https://pypi.python.org/pypi/pycannon)
[![PyPI Downloads](http://img.shields.io/pypi/dm/pycannon.svg)](https://pypi.python.org/pypi/pycannon)

A Python module for sending emails with [go-cannon](https://github.com/nathan-osman/go-cannon).

### Installation

Installing pycannon is as simple as:

    pip install pycannon

### Usage

Accessing the go-cannon API with pycannon centers around the `Connection` object. The example below demonstrates the process of creating an instance and using it to send a simple email:

    import pycannon

    c = pycannon.Connection()

    c.send(
        'me@me.com',
        ['you@you.com'],
        "Email Subject",
        "Plain text body.",
    )
