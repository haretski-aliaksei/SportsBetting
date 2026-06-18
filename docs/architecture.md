# Test Automation Framework Architecture

This document describes the architecture of the Sports Betting QA automation framework and the reasoning behind the main design choices.

## Goals

The framework is designed to be small enough for the assignment, but structured in a way that can grow without turning tests into hard-to-maintain scripts.

Main goals:

- keep tests readable and focused on business behavior
- separate UI, API, data, configuration, fixtures, and reporting concerns
- support local and CI execution
- support parallel execution without creating flaky tests around shared state
- make future extension predictable

## High-Level Layers

```text
tests/
  call page objects, API clients, fixtures, and test data

pages/
  provide browser-level business actions using Selenium

api/
  provide domain-specific API clients using requests

models/
  convert successful API responses into typed Python objects

test_data/
  stores business constants and runtime data factories

fixtures/
  provides settings, browser, API clients, and reporting hooks

config/
  stores environment files and runtime settings resolution

utils/
  contains shared helpers that do not belong to one specific layer
```

## Test Layer

Tests live under `tests/api/` and `tests/ui/`.

Tests should describe user or business behavior, not low-level implementation details. For example, a UI test should say that the user selects an odd, enters a stake, and places a bet. It should not contain raw Selenium locator logic.

Current tests:

- `tests/ui/test_bet_placement.py` covers bet placement behavior through the UI.
- `tests/api/test_bet_placement.py` validates bet placement behavior and business rules directly through the API.

Each test includes a docstring explaining why it was selected, as required by the assignment.

## UI Layer

UI automation uses the Page Object Model.

`pages/base_page.py` contains shared browser behavior:

- URL building
- page opening
- explicit waits
- common element lookup and click helpers

Page objects such as `pages/sportsbook_page.py` represent full pages. Each page can define a `PATH`, so new pages with different URL paths can be added without hardcoding URLs inside tests.

Reusable parts of a page live under `pages/components/`. The bet slip is modeled as `BetSlipComponent` because it is a reusable UI area with its own behavior.

This split keeps page objects smaller as the application grows.

## API Layer

API automation uses domain-specific clients instead of direct `requests` calls inside tests.

The API layer is split as follows:

- `api/base_client.py` handles shared request behavior.
- `api/clients/matches_client.py` handles match-related endpoints.
- `api/clients/balance_client.py` handles balance-related endpoints.
- `api/clients/bets_client.py` handles bet placement endpoints.
- `api/sportsbook_api.py` aggregates these clients behind one fixture-friendly object.

This design makes it easy to add new API domains later, for example users, betting history, promotions, or authentication.

## Models

Typed response models live in `models/sportsbook.py`.

Successful API responses are converted into dataclass objects such as:

- `Match`
- `Odds`
- `Balance`
- `PlaceBetResponse`

This avoids repeated dictionary access in tests and makes the API contract more visible. Monetary values are represented with `Decimal` to avoid floating-point precision issues.

## Test Data

Test data is separated into:

- `test_data/constants.py` for stable business constants such as stake limits and selections
- `test_data/factories.py` for generated runtime values such as valid stake amounts

The UI E2E test uses a generated valid stake amount within the allowed range. It also supports `TEST_STAKE_AMOUNT` as an environment override for reproducing a specific value.

## Fixtures

Fixtures are split by responsibility:

- `fixtures/settings.py` builds runtime settings and writes Allure environment metadata
- `fixtures/browser.py` creates and closes Chrome WebDriver
- `fixtures/api.py` creates the Sportsbook API client
- `fixtures/reporting.py` attaches UI failure evidence

`conftest.py` only registers fixture modules through `pytest_plugins`. This keeps the root test configuration compact and easier to scale.

## Configuration

Runtime settings are built in `config/settings.py`.

Default environment values live in `config/environments/staging.json`.

Settings can be overridden by:

- environment files
- environment variables
- pytest command-line options

This allows the same framework to run against different environments without changing test code.

## Reporting

Reporting is based on Allure.

Tests use `allure.step` blocks so failures show the exact business step that failed. Tests also include Allure labels:

- epic
- feature
- story
- severity

API tests attach request and response details for easier debugging.

UI failures attach:

- screenshot
- page source
- current URL
- page title

Allure environment metadata is written automatically when `--alluredir` is used.

## Tagging Strategy

Pytest markers are used to select meaningful test slices.

Markers are grouped by dimension:

- layer: `ui`, `api`
- purpose: `e2e`, `business_rule`, `validation`
- risk: `critical`
- suite: `smoke`, `regression`
- parallel state grouping: `xdist_group(name)`

Examples:

```bash
pytest -m critical
pytest -m "api and validation"
pytest -m "ui and e2e"
pytest -m "regression and not ui"
```

## Parallel Execution

Parallel execution uses `pytest-xdist`.

The project supports:

```bash
pytest --dist loadgroup -n auto
```

The current assignment environment uses one shared `USER_ID` and one mutable balance. Tests that touch this state are marked with:

```python
pytest.mark.xdist_group("balance_state")
```

With `--dist loadgroup`, these tests stay on the same worker and run safely in sequence. Future independent tests can still run in parallel.

## CI/CD

GitHub Actions is configured in `.github/workflows/tests.yml`.

The workflow:

- checks out the repository
- installs Python 3.12
- installs Google Chrome
- installs dependencies
- runs Ruff linting
- checks formatting
- runs tests in headless Chrome with Allure results
- uploads Allure results
- uploads failure screenshots when tests fail

This gives the project a basic quality gate for pull requests and pushes.

## Known Product Issue Handling

During testing, a product issue was observed: after a bet is placed, the backend balance is updated correctly, but the UI header balance is not refreshed.

Because of that known issue, the E2E UI test performs the critical user journey through the UI but verifies the final balance through the API. This keeps the test aligned with the real business outcome while avoiding a false failure caused by an already documented UI defect.

## How To Extend The Framework

To add a new UI page:

- create a page object under `pages/`
- define `PATH`
- add page-specific actions and locators
- move reusable widgets into `pages/components/`

To add a new API domain:

- create a new client under `api/clients/`
- expose it through `api/sportsbook_api.py`
- add typed models under `models/` when the response contract is stable

To add a new test:

- place it under `tests/ui/` or `tests/api/`
- use fixtures instead of manual setup
- use page objects or API clients instead of raw Selenium or requests
- use data from `test_data/`
- add meaningful pytest markers
- add Allure steps and a short selection rationale docstring

## Future Improvements

For a larger enterprise suite, the next improvements would be:

- isolated test users or seeded accounts for stronger parallelism
- richer API schema validation
- dedicated secret management in CI
- published Allure HTML report artifacts
- retry policy only for known infrastructure-level flakes
- more advanced logging and test run metadata
