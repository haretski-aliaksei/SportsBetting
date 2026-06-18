import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait

from pages.sportsbook_page import SportsbookPage
from test_data.factories import generate_valid_stake_amount


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.critical
@pytest.mark.regression
@pytest.mark.xdist_group("balance_state")
@allure.title("Place a home-win bet from the match list")
@allure.epic("Sports Betting")
@allure.feature("Single Bet Placement")
@allure.story("E2E bet placement")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description(
    "Critical E2E journey: the user selects a home-win odd in the UI, enters a stake, "
    "submits the bet, and the resulting server-side balance is verified through the API."
)
def test_user_can_place_home_win_bet_from_match_list(driver, settings, sportsbook_api):
    """Chosen because placing a bet is the critical journey across UI, API, and balance state."""
    stake = generate_valid_stake_amount()

    with allure.step("Reset user balance to make the E2E scenario independent"):
        sportsbook_api.balance.reset_balance()

    with allure.step("Capture the starting server-side balance"):
        balance_before = sportsbook_api.balance.get_balance().amount
        expected_balance = balance_before - stake

    page = SportsbookPage(driver, settings=settings)

    with allure.step("Open the sports betting page"):
        page.load()

    with allure.step("Select the first home-win odd from the match list"):
        page.select_first_home_win_odd()

    with allure.step(f"Enter stake amount: {stake} EUR"):
        page.bet_slip.enter_stake(str(stake))

    with allure.step("Submit the bet from the bet slip"):
        page.bet_slip.place_bet()

    with allure.step("Verify the backend balance is decreased by the stake amount"):
        WebDriverWait(driver, settings.timeout).until(
            lambda _: sportsbook_api.balance.get_balance().amount == expected_balance
        )
        actual_balance = sportsbook_api.balance.get_balance().amount
        assert actual_balance == expected_balance
