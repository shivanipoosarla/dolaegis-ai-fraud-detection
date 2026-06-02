# DolAegis Fraud Risk Report

Transactions analyzed: 6
High risk: 2
Manual review: 1
Approved: 3

## Transaction tx_1001
- User: `u_001`
- Score: **0/100**
- Risk level: **low**
- Decision: **approve**
- Factors: none

## Transaction tx_1002
- User: `u_002`
- Score: **100/100**
- Risk level: **high**
- Decision: **block**
- Factors:
  - `high_amount` +25: Transaction amount is at or above 1000.
  - `ip_billing_mismatch` +15: IP country differs from billing country.
  - `new_account` +15: Account is less than 7 days old.
  - `many_failed_logins` +20: Five or more failed login attempts were observed.
  - `velocity_spike` +20: Five or more transactions occurred in the last hour.
  - `new_device` +10: Transaction originated from a new device.
  - `high_risk_country` +15: Transaction is associated with a high-risk country flag.
  - `repeated_chargebacks` +20: User has two or more prior chargebacks.
  - `unusual_hour` +5: Transaction occurred between midnight and 5 AM.

## Transaction tx_1003
- User: `u_003`
- Score: **48/100**
- Risk level: **medium**
- Decision: **manual_review**
- Factors:
  - `medium_high_amount` +15: Transaction amount is at or above 500.
  - `billing_shipping_mismatch` +15: Billing and shipping countries differ.
  - `young_account` +8: Account is less than 30 days old.
  - `new_device` +10: Transaction originated from a new device.

## Transaction tx_1004
- User: `u_004`
- Score: **35/100**
- Risk level: **low**
- Decision: **approve**
- Factors:
  - `failed_login_spike` +10: Three or more failed login attempts were observed.
  - `elevated_velocity` +10: Three or more transactions occurred in the last hour.
  - `prior_chargeback` +10: User has one prior chargeback.
  - `unusual_hour` +5: Transaction occurred between midnight and 5 AM.

## Transaction tx_1005
- User: `u_005`
- Score: **0/100**
- Risk level: **low**
- Decision: **approve**
- Factors: none

## Transaction tx_1006
- User: `u_006`
- Score: **100/100**
- Risk level: **high**
- Decision: **block**
- Factors:
  - `medium_high_amount` +15: Transaction amount is at or above 500.
  - `ip_billing_mismatch` +15: IP country differs from billing country.
  - `new_account` +15: Account is less than 7 days old.
  - `velocity_spike` +20: Five or more transactions occurred in the last hour.
  - `new_device` +10: Transaction originated from a new device.
  - `high_risk_country` +15: Transaction is associated with a high-risk country flag.
  - `prior_chargeback` +10: User has one prior chargeback.
  - `unusual_hour` +5: Transaction occurred between midnight and 5 AM.
