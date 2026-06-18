from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from pages.components.base_component import BaseComponent


class BetSlipComponent(BaseComponent):
    SELECTED_HOME_WIN = (By.XPATH, "//*[contains(normalize-space(.), 'Match Winner: Home')]")
    STAKE_INPUT = (By.ID, "bet-slip-stake-input")
    PLACE_BET_BUTTON = (By.ID, "bet-slip-place-bet")

    def wait_for_home_win_selection(self) -> None:
        self.find_visible(self.SELECTED_HOME_WIN)

    def enter_stake(self, stake: str) -> None:
        stake_input = self.find_visible(self.STAKE_INPUT)
        stake_input.clear()
        stake_input.send_keys(stake)
        WebDriverWait(self.driver, self.timeout).until(lambda _: stake_input.get_attribute("value") == stake)

    def place_bet(self) -> None:
        WebDriverWait(self.driver, self.timeout).until(ec.element_to_be_clickable(self.PLACE_BET_BUTTON))
        self.click(self.PLACE_BET_BUTTON)
