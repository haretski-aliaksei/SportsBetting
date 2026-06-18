from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENTS_DIR = Path(__file__).parent / "environments"


@dataclass(frozen=True)
class Settings:
    env: str
    base_url: str
    api_url: str
    user_id: str
    browser: str
    headless: bool
    timeout: int


def build_settings(
    *,
    env: str | None = None,
    base_url: str | None = None,
    api_url: str | None = None,
    user_id: str | None = None,
    browser: str | None = None,
    headless: bool | None = None,
    timeout: int | None = None,
) -> Settings:
    resolved_env = env or os.getenv("ENV") or "staging"
    environment = _load_environment(resolved_env)
    resolved_base_url = (base_url or os.getenv("BASE_URL") or environment["base_url"]).rstrip("/")
    resolved_api_url = (api_url or os.getenv("API_URL") or environment.get("api_url") or resolved_base_url).rstrip("/")

    return Settings(
        env=resolved_env,
        base_url=resolved_base_url,
        api_url=resolved_api_url,
        user_id=user_id or os.getenv("USER_ID") or environment["user_id"],
        browser=browser or os.getenv("BROWSER") or environment.get("browser", "chrome"),
        headless=headless
        if headless is not None
        else _resolve_bool(os.getenv("HEADLESS"), environment.get("headless", False)),
        timeout=timeout or int(os.getenv("TIMEOUT") or environment.get("timeout", 10)),
    )


def _load_environment(env: str) -> dict[str, Any]:
    environment_file = ENVIRONMENTS_DIR / f"{env}.json"
    if not environment_file.exists():
        available = ", ".join(path.stem for path in sorted(ENVIRONMENTS_DIR.glob("*.json")))
        raise ValueError(f"Unknown environment '{env}'. Available environments: {available}")

    return json.loads(environment_file.read_text(encoding="utf-8"))


def _resolve_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.lower() == "true"
