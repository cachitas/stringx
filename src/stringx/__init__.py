"""
STRING API client using httpx.
"""

from __future__ import annotations  # required in Python 3.9

import typing

from .client import Client, __version__

__all__ = ["__version__", "Client"]

identity = ""


def map(
    identifiers: list[str],
    species: int,
    *,
    limit: int = 1,
    echo_query: bool = True,
) -> typing.Any:
    with Client(identity=identity) as client:
        return (
            client.map(
                identifiers=identifiers,
                species=species,
                limit=limit,
                echo_query=echo_query,
            )
            .raise_for_status()
            .json()
        )


def get_network(
    identifiers: list[str],
    species: int,
    *,
    required_score: float | None = None,
    network_type: str = "functional",
    add_nodes: int | None = None,
    show_query_node_labels: bool = False,
) -> typing.Any:
    with Client(identity=identity) as client:
        return (
            client.get_network(
                identifiers=identifiers,
                species=species,
                required_score=required_score,
                network_type=network_type,
                add_nodes=add_nodes,
                show_query_node_labels=show_query_node_labels,
            )
            .raise_for_status()
            .json()
        )


def get_interaction_partners(
    identifiers: list[str], species: int, limit: int | None = None
) -> typing.Any:
    with Client(identity=identity) as client:
        return (
            client.get_interaction_partners(
                identifiers=identifiers,
                species=species,
                limit=limit,
            )
            .raise_for_status()
            .json()
        )


def get_homology(identifiers: list[str], species: int) -> typing.Any:
    with Client(identity=identity) as client:
        return (
            client.get_homology(identifiers=identifiers, species=species)
            .raise_for_status()
            .json()
        )


def get_enrichment(
    identifiers: list[str],
    species: int,
    *,
    background_identifiers: list[str] | None = None,
) -> typing.Any:
    with Client(identity=identity) as client:
        return (
            client.get_enrichment(
                identifiers=identifiers,
                species=species,
                background_identifiers=background_identifiers,
            )
            .raise_for_status()
            .json()
        )


def get_version() -> typing.Any:
    with Client(identity=identity) as client:
        return client.get_version().raise_for_status().json()
