from __future__ import annotations

import pytest

from api.sportsbook_api import SportsbookApi
from config.settings import Settings


@pytest.fixture(scope="session")
def sportsbook_api(settings: Settings) -> SportsbookApi:
    return SportsbookApi(base_url=settings.api_url, user_id=settings.user_id)
