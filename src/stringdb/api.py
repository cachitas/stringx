import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class API:
    VERSION_ADDRESSES = {
        "12.0": "https://string-db.org/",
        "11.5": "https://version-11-5.string-db.org/",
        "11.0b": "https://version-11-0b.string-db.org/",
        "11.0": "https://version-11-0.string-db.org/",
        "10.5": "https://version-10-5.string-db.org/",
        "10.0": "https://version10.string-db.org/",
    }

    def __init__(self, version=None, client=None):
        self.client = client

        if version:
            self.stable_address = self.VERSION_ADDRESSES[version]
            self.version = version
        else:
            self.version = next(iter(self.VERSION_ADDRESSES))
            self.stable_address = self.VERSION_ADDRESSES[self.version]

    @property
    def api_url(self):
        return self.stable_address + "api"

    def _get(self, endpoint: str, params: dict = {}):
        url = "/".join([self.api_url, "json", endpoint])
        logger.info("GET", url, params)
        params.update(caller_identity=__name__)
        if self.client:
            response = self.client.get(url, params=params)
            logger.info(response.status_code)
            response.raise_for_status()
            return response.json()
        return (url, params)

    def get_string_ids(
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
        return self._get("get_string_ids", params=params)

    def get_interaction_partners(
        self,
        identifiers: List[str],
        species: int,
        # limit: Optional[int] = None,
    ):
        params = dict(
            identifiers="\r".join(identifiers),
            species=species,
            # limit=limit,
        )
        return self._get("interaction_partners", params=params)
