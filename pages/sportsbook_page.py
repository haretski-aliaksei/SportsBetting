from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.components.bet_slip_component import BetSlipComponent


class SportsbookPage(BasePage):
    PATH = "/"

    PAGE_TITLE = (By.XPATH, "//h1[contains(., 'Sports Betting QA')]")
    MATCHES_HEADING = (By.XPATH, "//h2[contains(., 'Upcoming Football Matches')]")
    BALANCE = (By.XPATH, "//*[starts-with(normalize-space(.), 'Balance:')]")
    MATCH_COUNTER = (
        By.XPATH,
        "//*[starts-with(normalize-space(.), 'Showing') and contains(normalize-space(.), 'matches')]",
    )
    ODDS_BUTTONS = (By.XPATH, "//button[.//*[normalize-space()='1' or normalize-space()='X' or normalize-space()='2']]")
    FIRST_HOME_ODDS = (By.XPATH, "(//button[contains(@id, '-home')])[1]")
    DATE_FILTER = (By.XPATH, "//button[contains(., 'Date:')]")
    ODDS_FILTER = (By.XPATH, "//button[contains(., 'Odds:')]")

    @property
    def bet_slip(self) -> BetSlipComponent:
        return BetSlipComponent(self.driver, self.timeout)

    def load(self) -> None:
        self.open_page(query_params={"user-id": self.settings.user_id})
        self.find_visible(self.PAGE_TITLE)
        self.find_visible(self.MATCH_COUNTER)

    def title(self) -> str:
        return self.text_of(self.PAGE_TITLE)

    def match_counter_text(self) -> str:
        return self.text_of(self.MATCH_COUNTER)

    def balance_text(self) -> str:
        return self.text_of(self.BALANCE)

    def odds_count(self) -> int:
        return len(self.find_all_visible(self.ODDS_BUTTONS))

    def has_filters(self) -> bool:
        return self.find_visible(self.DATE_FILTER).is_displayed() and self.find_visible(self.ODDS_FILTER).is_displayed()

    def select_first_home_win_odd(self) -> None:
        self.click(self.FIRST_HOME_ODDS)
        self.bet_slip.wait_for_home_win_selection()
