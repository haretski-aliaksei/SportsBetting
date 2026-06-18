from __future__ import annotations

import requests

from api.clients.balance_client import BalanceClient
from api.clients.bets_client import BetsClient
from api.clients.matches_client import MatchesClient


class SportsbookApi:
    def __init__(self, base_url: str, user_id: str, timeout: int = 10) -> None:
        session = requests.Session()
        self.matches = MatchesClient(base_url=base_url, user_id=user_id, timeout=timeout, session=session)
        self.balance = BalanceClient(base_url=base_url, user_id=user_id, timeout=timeout, session=session)
        self.bets = BetsClient(base_url=base_url, user_id=user_id, timeout=timeout, session=session)
