from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def assert_keys_present(payload: dict[str, Any], keys: Iterable[str]) -> None:
    missing_keys = set(keys) - set(payload)
    assert not missing_keys, f"Missing keys {missing_keys}. Payload: {payload}"
