from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class Odds:
    home: Decimal
    draw: Decimal
    away: Decimal

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> Odds:
        return cls(
            home=Decimal(str(payload["home"])),
            draw=Decimal(str(payload["draw"])),
            away=Decimal(str(payload["away"])),
        )


@dataclass(frozen=True)
class Match:
    id: str
    competition: str
    kickoff_date: str
    home_team: str
    away_team: str
    odds: Odds

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> Match:
        return cls(
            id=payload["id"],
            competition=payload["competition"],
            kickoff_date=payload["kickoffDate"],
            home_team=payload["homeTeam"],
            away_team=payload["awayTeam"],
            odds=Odds.from_dict(payload["odds"]),
        )


@dataclass(frozen=True)
class Balance:
    amount: Decimal
    currency: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> Balance:
        return cls(
            amount=Decimal(str(payload["balance"])),
            currency=payload["currency"],
        )


@dataclass(frozen=True)
class PlaceBetResponse:
    message: str
    match_id: str
    selection: str
    stake: Decimal
    odds: Decimal
    payout: Decimal
    balance: Decimal
    currency: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> PlaceBetResponse:
        return cls(
            message=payload["message"],
            match_id=payload["matchId"],
            selection=payload["selection"],
            stake=Decimal(str(payload["stake"])),
            odds=Decimal(str(payload["odds"])),
            payout=Decimal(str(payload["payout"])),
            balance=Decimal(str(payload["balance"])),
            currency=payload["currency"],
        )


@dataclass(frozen=True)
class ApiError:
    error: str
    message: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ApiError:
        return cls(error=payload["error"], message=payload["message"])
