import allure
import pytest

from models.sportsbook import ApiError
from test_data.constants import ABOVE_MAX_STAKE_AMOUNT, HOME_SELECTION
from utils.allure_helpers import attach_api_response

pytestmark = [
    pytest.mark.api,
    pytest.mark.business_rule,
    pytest.mark.validation,
    pytest.mark.critical,
    pytest.mark.regression,
    pytest.mark.xdist_group("balance_state"),
]


@allure.title("Reject a bet when stake is above the allowed maximum")
@allure.epic("Sports Betting")
@allure.feature("Single Bet Placement")
@allure.story("API stake validation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description(
    "Validates the place-bet API business rule: an oversized stake must be rejected "
    "and must not change the user's balance."
)
def test_place_bet_rejects_stake_above_allowed_maximum(sportsbook_api):
    """Chosen because maximum stake validation protects a core betting business rule and user balance integrity."""
    with allure.step("Get an available match to use in the bet request"):
        matches = sportsbook_api.matches.get_matches()
        match_id = matches[0].id

    with allure.step("Capture the current balance before the rejected operation"):
        balance_before = sportsbook_api.balance.get_balance().amount

    with allure.step("Try to place a bet with a stake above the allowed maximum"):
        response = sportsbook_api.bets.place_bet_response(
            match_id=match_id,
            selection=HOME_SELECTION,
            stake=ABOVE_MAX_STAKE_AMOUNT,
        )
        attach_api_response(response, name="Oversized stake place-bet response")

    with allure.step("Verify the API rejects the request with the expected validation error"):
        error = ApiError.from_dict(response.json())
        assert response.status_code == 422
        assert error.error == "invalid_stake_max"

    with allure.step("Verify the rejected bet did not change the balance"):
        assert sportsbook_api.balance.get_balance().amount == balance_before
