"""API client for the Hiring Challenge"""
import logging
import httpx

_API_BASE_URL = "https://bn-hiring-challenge.fly.dev"
_ENDPOINTS = {
    "members": "/members.json",
    "jobs": "/jobs.json",
}

log = logging.getLogger("client")


class BrightNetworkHiringChallengeClient:
    """Hiring Challenge API Client leveraging HTTPX"""

    def __init__(self) -> None:
        self._client = httpx.Client(base_url=_API_BASE_URL)

    def __del__(self) -> None:
        self._client.close()

    def _retrieve(self, what: str) -> list[dict[str, str]]:
        if what not in _ENDPOINTS:
            log.error("Endpoint %s not configured", what)
        response = self._client.get(_ENDPOINTS[what])
        try:
            return response.raise_for_status().json()
        except httpx.HTTPStatusError:
            log.error("Retrieving %s failed", what, exc_info=True)
        return []

    def retrieve_members(self) -> list[dict[str, str]]:
        """Retrieve member data"""
        return self._retrieve("members")

    def retrieve_jobs(self) -> list[dict[str, str]]:
        """Retrieve job data"""
        return self._retrieve("jobs")
