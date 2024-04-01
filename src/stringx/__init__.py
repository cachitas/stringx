"""
STRING API client using httpx.
"""

__version__ = "0.3.0"

from typing import List

from .client import Client

__all__ = ["Client"]

DEFAULT_CALLER_IDENTITY = f"{__name__} {__version__}"


def map_identifiers(identifiers: List[str], species: int):
    with Client() as client:
        return client.map_identifiers(identifiers=identifiers, species=species)


def network(identifiers: List[str], species: int):
    with Client() as client:
        return client.network(identifiers=identifiers, species=species)


def interaction_partners(identifiers: List[str], species: int):
    with Client() as client:
        return client.interaction_partners(identifiers=identifiers, species=species)
