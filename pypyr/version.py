"""Version information."""

import platform

__version__ = '0.3.2'


def get_version():
    return (f'pypyr {__version__} '
            f'python {platform.python_version()}')
