from __future__ import annotations

from decimal import Decimal

import requests

from api.base_client import BaseClient
from models.sportsbook import PlaceBetResponse


class BetsClient(BaseClient):
    def place_bet_response(self, match_id: str, selection: str, stake: Decimal | float | int) -> requests.Response:
        return self.post(
            "/api/place-bet",
            json={"matchId": match_id, "selection": selection, "stake": self._serialize_stake(stake)},
        )

    def place_bet(self, match_id: str, selection: str, stake: Decimal | float | int) -> PlaceBetResponse:
        response = self.place_bet_response(match_id=match_id, selection=selection, stake=stake)
        self.assert_status(response, 200)
        payload = response.json()
        assert isinstance(payload, dict), f"Expected place bet response to be an object, got {type(payload).__name__}"
        return PlaceBetResponse.from_dict(payload)

    def _serialize_stake(self, stake: Decimal | float | int) -> float | int:
        if isinstance(stake, Decimal):
            return int(stake) if stake == stake.to_integral_value() else float(stake)
        return stake
