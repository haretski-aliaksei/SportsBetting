from __future__ import annotations

import os
from decimal import Decimal
from random import randint

from test_data.constants import CENT, MAX_STAKE_AMOUNT, MIN_STAKE_AMOUNT


def generate_valid_stake_amount(
    min_amount: Decimal = MIN_STAKE_AMOUNT,
    max_amount: Decimal = MAX_STAKE_AMOUNT,
) -> Decimal:
    """Return a valid stake amount within the documented per-bet limits."""
    if stake_amount := os.getenv("TEST_STAKE_AMOUNT"):
        stake = Decimal(stake_amount).quantize(CENT)
        if not min_amount <= stake <= max_amount:
            raise ValueError(f"TEST_STAKE_AMOUNT must be between {min_amount} and {max_amount}")
        return stake

    min_cents = int(min_amount / CENT)
    max_cents = int(max_amount / CENT)
    return Decimal(randint(min_cents, max_cents)) * CENT
