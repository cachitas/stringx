"""
STRING API client using httpx.
"""

__version__ = "0.1.0"

from typing import List

from .client import Client

__all__ = ["Client"]

DEFAULT_CALLER_IDENTITY = f"{__name__} {__version__}"

