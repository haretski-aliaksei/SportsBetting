# Sports Betting QA Automation

Test automation framework for the Sports Betting QA assignment application.

## Tech Stack

- Python 3.12+
- Pytest
- Selenium WebDriver
- Python requests
- Latest desktop Chrome

## Additional Tooling

- `webdriver-manager` is used to resolve a compatible ChromeDriver automatically and simplify setup.
- `python-dotenv` is used to support optional local `.env` configuration without hardcoding environment-specific values.
- `allure-pytest` is used to produce step-based reports with screenshots and page source attached to failed UI tests.
- `pytest-xdist` is used for parallel test execution.
- `ruff` is used for linting, import ordering, and formatting checks.

## Application Under Test

- UI: `https://qae-assignment-tau.vercel.app/?user-id=candidate-ZAag5DNVYf`
- API docs: `https://qae-assignment-tau.vercel.app/api/docs#/`

## Project Deliverables

- [Test Plan - Single Bet Placement](docs/single_bet_placement_test_plan.md)
- [Bug Reports - Single Bet Placement](docs/single_bet_placement_bug_reports.md)
- [Strategy and Recommendations](docs/strategy_and_recommendations.md)
- [Framework Architecture](docs/architecture.md)
- Automation framework and tests are located under `tests/`, `pages/`, `api/`, and `config/`.

## Project Structure

```text
.
├── .github/workflows/    # GitHub Actions CI workflow
├── api/
│   ├── clients/          # Domain-specific API clients: matches, balance, bets
│   ├── base_client.py    # Shared requests behavior
│   └── sportsbook_api.py # Aggregates domain clients
├── config/
│   ├── environments/     # Environment JSON files, for example staging.json
│   └── settings.py       # Runtime settings resolution
├── docs/                 # Manual test deliverables for the assignment
├── fixtures/             # Pytest fixtures split by responsibility
├── models/               # Typed API response models
├── pages/
│   ├── components/       # Reusable UI components
│   ├── base_page.py      # Shared Selenium page behavior
│   └── sportsbook_page.py
├── reports/screenshots/  # Failure screenshots for UI tests
├── test_data/            # Test constants and data factories
├── tests/
│   ├── api/              # API tests
│   └── ui/               # UI tests
├── utils/                # Shared helpers
├── conftest.py           # Pytest plugin registration
├── pyproject.toml        # Ruff configuration
├── pytest.ini            # Pytest configuration and markers
├── requirements.txt      # Python dependencies
└── README.md
```

## Setup

Use Python 3.12 or newer. On macOS, prefer a Homebrew, pyenv, uv, or python.org Python build over the system Command Line Tools Python because the system build may use LibreSSL and emit urllib3 warnings.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Defaults are configured for the assignment environment:

```text
ENV=staging
BASE_URL=https://qae-assignment-tau.vercel.app
API_URL=https://qae-assignment-tau.vercel.app
USER_ID=candidate-ZAag5DNVYf
BROWSER=chrome
HEADLESS=false
TIMEOUT=10
```

Values can be overridden with environment variables, a local `.env` file, or pytest command-line options.

Environment files live under `config/environments/`. The default environment is `staging`:

```bash
pytest --env staging
```

Command-line options and environment variables override values loaded from the selected environment file.

If ChromeDriver cannot be downloaded automatically in a restricted environment, provide a local driver path:

```bash
export CHROMEDRIVER_PATH=/path/to/chromedriver
```

## Running Tests

Run all tests:

```bash
pytest
```

Run API tests only:

```bash
pytest -m api
```

Run UI tests only:

```bash
pytest -m ui
```

Run UI tests in headless Chrome:

```bash
pytest -m ui --headless
```

Run tests in parallel:

```bash
pytest --headless --dist loadgroup -n auto
```

The current assignment environment uses one shared `USER_ID`, so tests that touch the same mutable balance state are marked with `xdist_group("balance_state")`. With `--dist loadgroup`, those tests stay on the same worker and run safely in sequence, while independent tests can still be distributed across workers as the suite grows.

Run tests and collect Allure results:

```bash
pytest --alluredir=allure-results
```

The generated Allure report includes:

- step-by-step execution for each automated test
- epic, feature, story, and severity labels for test classification
- environment metadata such as selected environment, URLs, browser, timeout, Python version, and OS
- API request and response details for the API validation test
- screenshot, page source, current URL, and page title for failed UI tests

Serve the Allure report:

```bash
allure serve allure-results
```

The `allure` command requires the Allure CLI to be installed separately. On macOS, it can be installed with Homebrew:

```bash
brew install allure
```

Override URLs or user id:

```bash
pytest --base-url https://qae-assignment-tau.vercel.app --api-url https://qae-assignment-tau.vercel.app --user-id candidate-ZAag5DNVYf
```

## Code Quality

Run lint checks:

```bash
ruff check .
```

Check formatting:

```bash
ruff format --check .
```

Apply formatting:

```bash
ruff format .
```

## Architecture Decisions

The framework is intentionally organized by responsibility:

- UI automation uses Page Object Model classes under `pages/`.
- Reusable UI fragments live under `pages/components/`, so shared widgets such as the bet slip are not duplicated across page objects.
- API automation uses domain-specific clients under `api/clients/` instead of direct `requests` calls inside tests.
- Successful API responses are converted to typed dataclass models under `models/`.
- Test data is separated into constants and factories under `test_data/`.
- Pytest fixtures are split by concern under `fixtures/`: settings, browser, API, and reporting.
- Environment-specific configuration lives under `config/environments/` and can be overridden from CLI options or environment variables.

This keeps tests focused on business behavior while framework code handles browser setup, API communication, settings, data generation, and reporting.

## CI/CD

GitHub Actions workflow is defined in `.github/workflows/tests.yml`.

It runs on push, pull request, and manual dispatch:

```bash
pytest --env staging --headless --alluredir=allure-results --dist loadgroup -n auto -q
```

The workflow installs Python 3.12, Google Chrome, project dependencies, runs quality checks, runs the test suite in parallel, and uploads Allure results as an artifact. Failure screenshots are uploaded when UI tests fail.

Before running tests, CI also executes:

```bash
ruff check .
ruff format --check .
```

CI is configured as a quality gate for pull requests and pushes to `main` or `master`.

## Pytest Markers

- `ui` - browser-based tests using Selenium WebDriver
- `api` - HTTP API tests using requests
- `e2e` - complete user journeys across UI and backend state
- `business_rule` - checks for domain-specific betting rules
- `validation` - negative or boundary validation checks
- `critical` - highest-priority tests that protect core product or business risk
- `smoke` - high-value availability checks
- `regression` - broader regression coverage
- `xdist_group(name)` - tests that share mutable state and must stay on the same parallel worker

Markers are organized by several dimensions:

- test layer: `ui`, `api`
- test purpose: `e2e`, `business_rule`, `validation`
- risk priority: `critical`
- suite scope: `smoke`, `regression`

Examples:

```bash
pytest -m critical
pytest -m "api and validation"
pytest -m "ui and e2e"
pytest -m "regression and not ui"
```

## Framework Design

UI tests use the Page Object Model. Common browser actions and explicit waits live in `pages/base_page.py`; page-specific locators and behaviors live in page classes such as `pages/sportsbook_page.py`.

Each page object can define its own `PATH`, while `BasePage` builds URLs from `BASE_URL`, the page path, and optional query parameters. This keeps tests independent from concrete URL construction and makes it easier to add pages such as `/history`, `/profile`, or `/login` later.

Reusable UI areas are modeled as components under `pages/components/`. For example, bet slip actions such as entering a stake and placing a bet live in `BetSlipComponent` instead of the full page object.

API tests use client classes instead of calling `requests` directly from tests. `api/base_client.py` handles shared request behavior, while domain clients under `api/clients/` expose assignment-specific endpoints for matches, balance, and bets.

API clients return typed dataclass models from `models/` for successful responses. This avoids repeated dictionary key access in tests and makes the API contract easier to understand and extend.

Test data lives in `test_data/`. Business constants such as stake limits and selections are separated from factories that generate valid runtime values. This keeps tests readable and makes boundary/negative data easier to reuse.

Shared setup is centralized in `conftest.py`:

- registers fixture modules from `fixtures/`
- builds runtime settings
- creates the Selenium Chrome driver
- creates the Sportsbook API client
- saves screenshots for failed UI tests and attaches screenshot/page source to Allure reports

Reporting is built around Allure. Tests include readable `allure.step` blocks, business-oriented descriptions, and labels such as epic, feature, story, and severity. API tests attach request and response details. UI failures attach browser evidence to make debugging faster.

Parallel execution uses `pytest-xdist`. Because the assignment environment currently provides one shared `USER_ID`, tests that touch mutable balance state are grouped with `xdist_group("balance_state")`. This keeps shared-state tests stable while allowing future independent tests to run on separate workers.

## Current Test Coverage

The current tests focus on the two high-value checks requested by the assignment:

- E2E UI journey: user selects a home-win odd from the match list, enters a stake, places the bet, and the server-side balance is updated
- API rejects a bet above the allowed maximum stake and keeps the balance unchanged

The API test intentionally uses `POST /api/place-bet` instead of a simple read-only endpoint. It validates a betting business rule directly through the API: stakes above the maximum allowed value must be rejected with a validation error and must not affect the user's balance.

Known issue observed during test design: after a bet is placed, the backend balance is updated correctly, but the UI balance displayed in the page header is not refreshed. For that reason, the E2E test performs the user journey through the UI and verifies the final business state through the API.

More detailed business scenarios can be added next, including filtering, successful bet placement, balance updates, reset balance, negative API cases, and API/UI consistency checks.

## Scalability Notes

The project already includes several practices that help it grow beyond a small assignment:

- domain-oriented API clients
- reusable UI components
- typed response models
- centralized test data constants and factories
- fixture modules split by concern
- environment files and CLI overrides
- GitHub Actions CI
- Ruff linting and formatting
- Allure reporting with execution evidence
- marker-based test selection
- xdist-based parallel execution with shared-state grouping

For a larger enterprise suite, the next natural additions would be richer schema validation, more isolated test users or seeded test accounts, secret management in CI, test retry policy for known infrastructure flakes, and published Allure HTML reports.
