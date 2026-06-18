# Strategy and Recommendations

## Why These 2 Tests Were Selected for Automation

The assignment asks for two high-value automated tests rather than exhaustive coverage. I selected one UI E2E test and one API business-rule validation test to balance business value, maintainability, and test pyramid principles.

### 1. E2E UI Test - Successful Single Bet Placement

I selected the successful single bet placement flow as the UI E2E automated test because it represents the most business-critical user journey in the application.

This test covers the customer-facing betting flow:

- opening the application as a user with a valid user context
- selecting an upcoming football match
- selecting one available outcome
- entering a valid stake amount
- placing the bet
- verifying that the server-side balance is decreased by the stake amount

This scenario was prioritized because placing a bet is the core product flow. If this flow is broken, the main purpose of the application is broken as well.

From an automation perspective, this test provides high value because it works as a smoke and regression check for the full betting path. It validates that the UI, match list, bet slip, bet submission flow, API state, and balance update are connected and functioning together.

I intentionally selected only one UI E2E test because UI tests are usually more expensive to maintain than API tests. They are slower, more sensitive to layout changes, and more likely to fail due to timing or locator issues. Therefore, I chose a single high-value UI test that gives strong business coverage instead of automating many smaller UI checks.

This test is a good automation candidate because:

- it validates the most important happy path
- it covers several components working together
- it provides fast feedback if the core betting flow is broken
- it can be used as a release smoke test
- it is easy to understand and valuable for both QA and non-QA stakeholders

Known product behavior was also considered. During testing, I observed that after a bet is placed, the backend balance is updated correctly, but the UI header balance is not refreshed. Because that UI issue is already documented as a defect, the E2E test performs the user journey through the UI and verifies the final business state through the API.

### 2. API Test - Maximum Stake Validation

I selected maximum stake validation as the API automated test because financial validation must be enforced on the backend, regardless of what happens in the UI.

The specification states that the maximum stake per bet is `EUR 100.00` and that both UI and API should reject invalid stake values. This makes max-stake validation a high-risk business rule and a strong candidate for API-level automation.

This test sends a direct API request to place a bet with a stake amount greater than the allowed maximum. The expected behavior is that the API rejects the request with a validation error and does not change the user's balance.

This test was selected because it protects a critical financial rule:

- users must not be able to place bets above the configured stake limit
- invalid bet attempts must not affect account balance
- backend validation must not rely only on UI restrictions
- API behavior must be consistent with business rules and product expectations

I selected this scenario for API automation rather than UI automation because negative financial validation is more stable and efficient to verify directly through the backend. API tests are faster, easier to run in CI, less flaky than UI tests, and better suited for validating business rules and edge cases.

This test is a good automation candidate because:

- it verifies a high-risk financial rule
- it validates backend protection directly
- it is faster and more stable than testing the same rule only through UI
- it can prevent serious regressions
- it clearly demonstrates separation between UI E2E coverage and API business-rule coverage

Together, these two tests provide complementary coverage:

- the UI test validates that the main customer journey works end to end
- the API test validates that server-side financial rules are enforced
- the combination gives better coverage than two UI tests or two isolated happy-path API tests
- the approach demonstrates that not every scenario should be automated at the same level

Other scenarios were valuable, but I did not select them as the first automation candidates because they either require more complex test data handling, are better suited for manual exploration, or are less stable for a small take-home automation framework.

## What Was Intentionally Left as Manual Only and Why

### 1. Date Filter and Past Events Testing

Past-events and date-filter testing were intentionally left as manual and exploratory testing for the initial automation scope.

This area is important because users should not be able to place bets on completed or invalid events. However, date-based scenarios can be sensitive to the current system date, test data availability, timezone handling, and dynamic match lists.

This scenario is a strong candidate for future automation once the test environment provides stable test data or controllable dates.

For now, I would keep it manual because:

- it requires careful verification of date picker behavior
- it depends on current date and available events
- it involves both UI filtering and business-rule validation
- it benefits from exploratory observation
- it may require controlled backend fixtures to make automation reliable

### 2. Stake Boundary Validation Matrix

Stake boundary validation was intentionally left mostly manual for the initial scope.

The test plan includes important values such as empty value, `0`, `0.99`, `1.00`, `1.01`, `100.00`, `100.01`, values with more than two decimal places, non-numeric input, and negative values. These checks are valuable, but automating all of them in the first version would make the small framework larger without necessarily improving the assignment result.

I would automate these later as parameterized API tests once the core API client, test data strategy, and expected validation responses are stable.

For the initial version, I left this manual because:

- there are many input combinations
- some values require specification clarification
- API parameterization would be better added after the basic framework is in place
- the assignment values automation quality over quantity

### 3. Duplicate Bet Placement and Race Condition Checks

Duplicate bet placement was intentionally left manual or exploratory.

This scenario checks whether the system prevents multiple bet submissions while a request is already in progress. It is high risk because duplicate bets may cause double stake deduction or incorrect balance updates.

Reliable automation for this scenario may require parallel requests, network throttling, synchronization, or lower-level API concurrency tests. In a small take-home project, this would add complexity and could make the tests flaky.

I would not include it in the first automation version because:

- race-condition tests are harder to make deterministic
- they may require special tooling or concurrency control
- UI double-click behavior can be timing-sensitive
- it is better suited for a dedicated reliability or API concurrency test layer later

### 4. Visual Checks and Receipt Layout Verification

Detailed visual checks were intentionally left manual.

The receipt should display Bet ID, match details, selection, stake, odds, potential payout, and timestamp. Automation can check key values, but visual alignment, readability, formatting quality, and user perception are better validated manually or with dedicated visual regression tooling.

For the initial framework, I would avoid strict visual assertions because:

- they are brittle
- they can fail due to minor styling changes
- they require additional tooling not necessary for the assignment
- they are better covered by manual review or visual regression tools in a mature pipeline

### 5. Error Modal Behavior

Error modal behavior was also left manual for now.

The specification describes an error modal with Rebet, Close, and top-right X behavior. This is important, but it requires forcing specific backend failures or network failures. Without a controlled way to trigger errors, automated tests may become unstable or dependent on artificial conditions.

I would automate this later if the application provides a test hook, mock mode, or controlled API failure response.

## Top Recommendations If This Project Were To Scale

The current framework already includes a scalable foundation: clean project structure, Page Object Model, reusable UI components, domain-specific API clients, typed response models, centralized test data, split fixtures, environment-based configuration, Allure reporting, marker-based test selection, parallel execution support, CI/CD, and Ruff quality checks.

If this project were to scale further, I would focus on the following areas.

### 1. Strengthen Test Data Strategy and State Isolation

The current test environment uses a shared user context and shared balance state. The framework mitigates this with balance reset and xdist grouping, but a larger suite would need stronger test data isolation.

Recommended improvements:

- dedicated test users per scenario or per parallel worker
- seeded accounts with known balances
- deterministic match data for boundary and filtering scenarios
- API test hooks for preparing and cleaning up state

This would reduce flaky tests, improve parallel execution, and make negative and boundary scenarios easier to automate reliably.

### 2. Expand API and Contract Coverage Before Growing UI Coverage

Before adding many more UI tests, I would expand the API and contract layers because they are faster, more stable, and better suited for business-rule validation.

Recommended improvements:

- parameterized API tests for stake boundaries and precision
- selection and match validation tests
- malformed payload, unauthorized user, and method-not-allowed checks
- response schema validation against the OpenAPI contract

This would give broad validation coverage without creating a slow or brittle UI-heavy regression suite.

### 3. Clarify Ambiguous Requirements and Add Testability Hooks

Several scenarios would benefit from clearer specification or better testability support before automation is expanded.

Recommended clarifications:

- exact minimum stake rule and expected validation message
- exact API error codes and response bodies for each validation failure
- expected behavior for duplicate submissions and `409 bet already in progress`
- controlled way to trigger error modal and retry behavior
- expected receipt formatting for timestamp, payout rounding, and currency display

This would make future automated tests more deterministic and reduce disagreement between QA, product, and engineering about expected behavior.
