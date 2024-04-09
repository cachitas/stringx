from __future__ import annotations  # required in Python 3.9

import logging

import httpx

__version__ = "0.6.0"

logger = logging.getLogger("stringx")


class Client(httpx.Client):
    def __init__(self, identity: str, base_url: str = "https://string-db.org") -> None:
        if not identity:
            raise ValueError("Client identity must be a non-empty string.")

        self.identity = f"{identity} (python-stringx/{__version__})"

        self.format = "json"

        super().__init__(
            params={"caller_identity": self.identity},
            base_url=base_url,
        )

    def _update_metadata(self) -> None:
        data = self.get_version().json()
        self._version: str = data[0]["string_version"]
        self._stable_address: str = data[0]["stable_address"]

    @property
    def version(self) -> str:
        try:
            return self._version
        except AttributeError:
            self._update_metadata()
            return self._version

    @property
    def stable_address(self) -> str:
        try:
            return self._stable_address
        except AttributeError:
            self._update_metadata()
            return self._stable_address

    def map(
        self,
        identifiers: list[str],
        species: int,
        *,
        limit: int = 1,
        echo_query: bool = True,
        format: str | None = None,
    ) -> httpx.Response:
        url = f"api/{format or self.format}/get_string_ids"

        params = httpx.QueryParams(
            identifiers="\r".join(identifiers),
            species=species,
            limit=limit,
            echo_query=echo_query,
        )

        return self.post(url, params=params)

    def network(
        self,
        identifiers: list[str],
        species: int,
        *,
        required_score: float | None = None,
        network_type: str = "functional",
        add_nodes: int | None = None,
        show_query_node_labels: bool = False,
        format: str | None = None,
    ) -> httpx.Response:
        url = f"api/{format or self.format}/network"

        params = httpx.QueryParams(
            identifiers="\r".join(identifiers),
            species=species,
            network_type=network_type,
            show_query_node_labels=int(show_query_node_labels),
        )

        if required_score:
            params = params.add("required_score", required_score)

        if add_nodes:
            params = params.add("add_nodes", add_nodes)

        return self.post(url, params=params)

    def interaction_partners(
        self,
        identifiers: list[str],
        species: int,
        *,
        limit: int | None = None,
        format: str | None = None,
    ) -> httpx.Response:
        url = f"api/{format or self.format}/interaction_partners"

        params = httpx.QueryParams(
            identifiers="\r".join(identifiers),
            species=species,
        )

        if limit:
            params = params.add("limit", limit)

        return self.post(url, params=params)

    def homology(
        self, identifiers: list[str], species: int, *, format: str | None = None
    ) -> httpx.Response:
        url = f"api/{format or self.format}/homology"

        params = httpx.QueryParams(
            identifiers="\r".join(identifiers),
            species=species,
        )

        return self.post(url, params=params)

    def enrichment(
        self,
        identifiers: list[str],
        species: int,
        *,
        background_identifiers: list[str] | None = None,
        format: str | None = None,
    ) -> httpx.Response:
        url = f"api/{format or self.format}/enrichment"

        params = httpx.QueryParams(
            identifiers="\r".join(identifiers),
            species=species,
        )
        if background_identifiers:
            params = params.add(
                "background_string_identifiers", "\r".join(background_identifiers)
            )

        return self.post(url, params=params)

    def get_version(self, *, format: str | None = None) -> httpx.Response:
        request = self.build_request("GET", f"api/{format or self.format}/version")
        request.url = request.url.copy_remove_param("caller_identity")
        return self.send(request)
