# Test Plan - Single Bet Placement

## Scope

This test plan covers the Single Bet Placement feature for a desktop web application. The focus is on the core betting flow, financial validations, boundary conditions, and high-risk user scenarios.

## Scenarios

### TC-001 - Successful Single Bet Placement

**Priority:** Critical

**Risk Rationale:**  
This is the core revenue-generating user journey. If a user cannot successfully place a valid bet, the primary business functionality of the application is broken. The scenario also validates financial consistency between the selected odds, stake, receipt details, and updated balance.

**Steps:**
1. Open the application as a logged-in user.
2. Select an upcoming football match.
3. Select one available outcome: `1`, `X`, or `2`.
4. Enter a valid stake amount, for example `10.00`, in the Stake input field within the bet slip.
5. Verify that the bet slip displays the selected match, selection, odds, available balance, and potential payout.
6. Click `Place Bet`.
7. Wait for the placement process to complete.
8. Verify the success receipt and updated balance.

**Expected Result:**
- The bet is successfully placed.
- The `Place Bet` button enters the `Placing...` state during submission.
- The stake amount is deducted from the available balance.
- A success receipt is displayed.
- The receipt contains Bet ID, match details, selection, stake, odds at placement, potential payout, and placement timestamp.
- The receipt data matches the information shown before placement.
- Closing the receipt returns the user to the main flow without an active selection.

### TC-002 - Prevent Bet Placement on Past Events

**Priority:** Critical

**Risk Rationale:**  
Only upcoming/pre-match events should be available for betting. Allowing users to place bets on past matches creates invalid betting activity, financial risk, and loss of trust in the platform.

**Steps:**
1. Open the application as a logged-in user.
2. Open the Date filter.
3. Try to select a past date or a date range that includes past dates.
4. Click `Apply`.

**Expected Result:**
- The user cannot apply a date filter that includes past dates.
- Past dates are disabled in the date picker or the system shows a clear validation message.
- The match list does not display events with kickoff dates earlier than the current date/time.
- No past event is selectable for betting.
- The user cannot add a past event to the bet slip or place a bet on it.

### TC-003 - Reject Stake Exceeding Available Balance

**Priority:** Critical

**Risk Rationale:**  
The system must prevent users from placing bets above their available balance. Failure to enforce this rule may lead to invalid financial state, incorrect bet acceptance, and financial disputes.

**Steps:**
1. Open the application as a logged-in user.
2. Verify the available balance.
3. Select an upcoming football match.
4. Select one available outcome.
5. Enter a stake amount greater than the available balance in the Stake input field within the bet slip.
6. Click `Place Bet`.

**Expected Result:**
- Bet placement is blocked.
- The stake amount is not deducted.
- No success receipt is generated.
- The user sees a clear validation message indicating insufficient balance.
- The balance remains unchanged in both the header and the bet slip.

### TC-004 - Stake Boundary Validation

**Priority:** High

**Risk Rationale:**  
Stake validation protects the platform from invalid financial input. Boundary validation defects may result in incorrect bet acceptance or rejection, financial inconsistencies, and poor user experience.

**Steps:**
1. Open the application as a logged-in user.
2. Select an upcoming football match.
3. Select one available outcome.
4. Enter the following stake values one by one:
   - empty value
   - `0`
   - `0.99`
   - `1.00`
   - `1.01`
   - `100.00`
   - `100.01`
   - `1.111`
   - `abc`
   - `-1`
5. Observe validation behaviour and attempt to place a bet where applicable.

**Expected Result:**
- Empty stake is rejected.
- Non-numeric values are rejected.
- Negative and zero values are rejected.
- Stake values above the maximum limit are rejected.
- Values with more than two decimal places are rejected.
- Valid boundary values are accepted according to the agreed business rules.
- Validation behaviour is consistent between the UI and API.

### TC-005 - Replace Previous Selection with New Odds Selection

**Priority:** High

**Risk Rationale:**  
The feature supports single bets only, therefore the system must maintain exactly one active selection at any time. Incorrect selection replacement may lead to placing bets on the wrong outcome or displaying incorrect payout information.

**Steps:**
1. Open the application as a logged-in user.
2. Select outcome `1` for one football match.
3. Verify that the selection appears in the bet slip.
4. Select outcome `X` for the same or another match.
5. Verify that the previous selection is replaced.
6. Select outcome `2`.
7. Verify the bet slip again.

**Expected Result:**
- Only one active selection is available at any time.
- Each new odds selection replaces the previous one.
- The bet slip displays the latest selected match, outcome, and odds.
- The previous selection is visually deselected.
- The potential payout is recalculated based on the latest selected odds.
- No multiple selections are accumulated.

### TC-006 - Prevent Duplicate Bet Placement While Request Is In Progress

**Priority:** High

**Risk Rationale:**  
Duplicate bet placement can cause double stake deduction, duplicate bets, incorrect balance state, and financial disputes. Since bet placement is a financial transaction, the system must prevent repeated submissions while a placement request is already in progress.

**Steps:**
1. Open the application as a logged-in user.
2. Select an upcoming football match.
3. Select one available outcome.
4. Enter a valid stake amount, for example `10.00`.
5. Click `Place Bet`.
6. Immediately click `Place Bet` again or double-click the button quickly.
7. Observe the UI behaviour and final result.

**Expected Result:**
- The `Place Bet` button enters the `Placing...` loading state.
- Additional placement attempts are blocked while the request is in progress.
- Only one bet is created.
- The stake amount is deducted only once.
- Only one success receipt or one error result is displayed.
- If the API receives a duplicate in-progress request, it returns `409 - Bet already in progress`.
- The final UI state resolves to one clear outcome: success or failure.
