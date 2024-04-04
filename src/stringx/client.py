import logging

import httpx

__version__ = "0.3.0"

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

    def map(
        self,
        identifiers: list[str],
        species: int,
        *,
        limit: int = 1,
        echo_query: bool = True,
        format: str | None = None,
    ):
        url = f"api/{format or self.format}/get_string_ids"

        params = {
            "identifiers": "\r".join(identifiers),  # your protein list
            "species": species,  # species NCBI identifier
            "limit": limit,  # only one (best) identifier per input protein
            "echo_query": echo_query,  # see your input identifiers in the output
        }

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
    ):
        url = f"api/{format or self.format}/network"

        params = {
            "identifiers": "\r".join(identifiers),
            "species": species,
            "network_type": network_type,
            "show_query_node_labels": int(show_query_node_labels),
        }

        if required_score:
            params |= {"required_score": required_score}

        if add_nodes:
            params |= {"add_nodes": add_nodes}

        return self.post(url, params=params)

    def interaction_partners(
        self,
        identifiers: list[str],
        species: int,
        *,
        limit: int | None = None,
        format: str | None = None,
    ):
        url = f"api/{format or self.format}/interaction_partners"

        params = {
            "identifiers": "\r".join(identifiers),
            "species": species,
        }

        if limit:
            params.update(limit=limit)

        return self.post(url, params=params)

    def homology(
        self, identifiers: list[str], species: int, *, format: str | None = None
    ):
        url = f"api/{format or self.format}/homology"

        params = {
            "identifiers": "\r".join(identifiers),
            "species": species,
        }

        return self.post(url, params=params)

    def version(self) -> str:
        request = self.build_request("GET", "api/json/version")
        request.url = request.url.copy_remove_param("caller_identity")
        return self.send(request).json()
