from __future__ import annotations

from typing import Any

import requests


class ApiResponseError(AssertionError):
    pass


class BaseClient:
    def __init__(
        self,
        base_url: str,
        user_id: str,
        timeout: int = 10,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "x-user-id": user_id,
            }
        )

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.session.get(self._url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str, json: dict[str, Any] | None = None, **kwargs: Any) -> requests.Response:
        return self.session.post(self._url(path), json=json, timeout=self.timeout, **kwargs)

    def assert_status(self, response: requests.Response, expected_status: int) -> None:
        if response.status_code != expected_status:
            raise ApiResponseError(
                f"Expected status {expected_status}, got {response.status_code}. Response body: {response.text}"
            )

    def _url(self, path: str) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{normalized_path}"
