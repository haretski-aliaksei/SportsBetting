# Bug Reports - Single Bet Placement Feature

**Application:** Single Bet Placement Assignment  
**Environment:** Web Application + Swagger API (`/api/docs`)  
**Tester:** Aliaksei Haretski  
**Date:** 17 June 2026

## BUG-001 - Application Allows Users to Place Bets with a Negative Account Balance

**Severity:** Critical

### Reproduction Steps

1. Open the application as a logged-in user.
2. Verify that the current available balance is `EUR 120`.
3. Select any upcoming football match.
4. Select any available outcome.
5. Enter the maximum stake amount, `EUR 100`, in the Stake field.
6. Click `Place Bet`.
7. Wait for the bet to be placed successfully.
8. Verify that the balance displayed in the UI remains `EUR 120` and has not been reduced after the funds were deducted.
9. Open Swagger UI and verify the user's actual balance. Confirm that the server-side balance is `EUR 20`.
10. Select another upcoming football match.
11. Select any available outcome.
12. Enter a stake amount of `EUR 100` and click `Place Bet`.
13. Open Swagger UI again and verify the user's actual balance. Confirm that the server-side balance has become negative.

### Expected Result

- After a successful bet placement, the user's balance should be updated immediately in the UI.
- After the first bet, the available balance should decrease from `EUR 120` to `EUR 20`.
- The user should not be able to place a second bet of `EUR 100` because it exceeds the remaining available balance.
- The account balance should never become negative.
- The user should see a clear validation message when there are insufficient funds.

### Actual Result

- After the first bet, the balance displayed in the UI remains `EUR 120` and does not reflect the actual deduction of funds.
- Additional verification via Swagger shows that the actual server-side balance is already `EUR 20`.
- The user continues to see the original balance and is able to place a second bet of `EUR 100`, which exceeds the actual available balance.
- After the second bet, the actual account balance becomes negative.
- Additional verification via Swagger confirms the negative server-side balance.
- The application continues to allow users to place bets despite the negative balance.

### Business Impact

The user receives incorrect information about the available funds and can place bets that exceed the actual account balance. As a result, the system allows negative balances, which violates fundamental financial rules of a betting platform and may lead to financial losses, inaccurate reporting, calculation errors, and disputes with users.

### Evidence

[Video reproduction](https://drive.google.com/file/d/1AsHfPu3k1cPiiFIZ85s8wDsNYBtOUJxp/view?usp=sharing)

## BUG-002 - User Can Place Bets on Past Events

**Severity:** Critical

### Reproduction Steps

1. Open the application as a logged-in user.
2. Open the Date filter.
3. Select a past date or a date range that includes past dates.
4. Click `Apply`.
5. Verify that events with kickoff times earlier than the current date and time are displayed.
6. Select any available outcome for one of the displayed events.
7. Enter a valid stake amount in the Stake field.
8. Click `Place Bet`.

### Expected Result

- Users should not be able to select dates in the past.
- Events with kickoff times earlier than the current date and time should not be displayed for betting.
- Users should not be able to add past events to the Bet Slip.
- Users should not be able to place bets on completed events.

### Actual Result

- The application allows users to select dates in the past.
- Completed events are displayed after applying the filter.
- Users can select outcomes for completed events.
- The application successfully accepts and places bets on completed events.

### Business Impact

Allowing users to place bets on completed events violates a fundamental business rule of a betting platform. Users can place bets knowing the outcome of an event, which creates an opportunity for abuse and guaranteed winnings, exposes the operator to direct financial losses, and significantly undermines trust in the platform.

### Evidence

[Video reproduction](https://drive.google.com/file/d/1gpx1lEoisJ5YoAk13bASWY4Cexa_pRGq/view?usp=sharing)
