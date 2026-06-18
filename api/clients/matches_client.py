from __future__ import annotations

from api.base_client import BaseClient
from models.sportsbook import Match


class MatchesClient(BaseClient):
    def get_matches(self) -> list[Match]:
        response = self.get("/api/matches")
        self.assert_status(response, 200)
        payload = response.json()
        assert isinstance(payload, list), f"Expected matches response to be a list, got {type(payload).__name__}"
        return [Match.from_dict(item) for item in payload]
