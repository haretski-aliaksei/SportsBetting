from __future__ import annotations

from api.base_client import BaseClient
from models.sportsbook import Balance


class BalanceClient(BaseClient):
    def get_balance(self) -> Balance:
        response = self.get("/api/balance")
        self.assert_status(response, 200)
        payload = response.json()
        assert isinstance(payload, dict), f"Expected balance response to be an object, got {type(payload).__name__}"
        return Balance.from_dict(payload)

    def reset_balance(self) -> Balance:
        response = self.post("/api/reset-balance")
        self.assert_status(response, 200)
        payload = response.json()
        assert isinstance(payload, dict), f"Expected reset response to be an object, got {type(payload).__name__}"
        return Balance.from_dict(payload)
