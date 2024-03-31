import logging
from typing import List, Optional

import httpx


logger = logging.getLogger(__name__)


class Client(httpx.Client):
    def __init__(
        self, base_url: str = "https://string-db.org", *, identity: Optional[str] = None
    ) -> None:
        from stringx import DEFAULT_CALLER_IDENTITY

        super().__init__(
            params=dict(caller_identity=identity or DEFAULT_CALLER_IDENTITY),
            base_url=base_url,
        )

    def request(
        self,
        endpoint: str,
        params: dict = {},
        *,
        method: str = "POST",
        format: str = "json",
    ):
        url = "/".join(["api", format, endpoint])
        logger.info("POST", url, params)
        response = super().request(method, url, params=params)
        logger.info(response.status_code)
        response.raise_for_status()
        return response.json()

    def map_identifiers(
        self,
        identifiers: List[str],
        species: int,
        limit: int = 1,
        echo_query: bool = True,
    ):
        params = {
            "identifiers": "\r".join(identifiers),  # your protein list
            "species": species,  # species NCBI identifier
            "limit": limit,  # only one (best) identifier per input protein
            "echo_query": echo_query,  # see your input identifiers in the output
        }
        return self.request("get_string_ids", params=params)

    def network(
        self,
        identifiers: List[str],
        species: int,
        required_score: Optional[float] = None,
        network_type: str = "functional",
        add_nodes: Optional[int] = None,
        show_query_node_labels: bool = False,
    ):
        params = dict(
            identifiers="\r".join(identifiers),
            species=species,
            network_type=network_type,
            show_query_node_labels=int(show_query_node_labels),
        )

        if required_score:
            params |= {"required_score": required_score}

        if add_nodes:
            params |= {"add_nodes": add_nodes}

        return self.request("network", params=params)

    def interaction_partners(
        self,
        identifiers: List[str],
        species: int,
        limit: Optional[int] = None,
    ):
        params = dict(
            identifiers="\r".join(identifiers),
            species=species,
        )

        if limit:
            params.update(limit=limit)

        return self.request("interaction_partners", params=params)
