
// Core DAX Measures

Total Clients = DISTINCTCOUNT(dim_client[client_id])

Total Loan Amount = SUM(fact_banking_relationship[loan_amount])

Total Deposit Amount = SUM(fact_banking_relationship[deposit_amount])

Default Rate % =
DIVIDE(
    COUNTROWS(FILTER(fact_banking_relationship, fact_banking_relationship[default_flag] = 1)),
    COUNTROWS(fact_banking_relationship)
) * 100

LTD Ratio = DIVIDE([Total Loan Amount], [Total Deposit Amount])

High Risk Clients =
COUNTROWS(FILTER(fact_banking_relationship, fact_banking_relationship[risk_score] >= 71))

Avg Risk Score = AVERAGE(fact_banking_relationship[risk_score])

Avg Credit Score = AVERAGE(fact_banking_relationship[credit_score])

Loan Growth YoY =
DIVIDE(
    [Total Loan Amount] - CALCULATE([Total Loan Amount], SAMEPERIODLASTYEAR(dim_date[date])),
    CALCULATE([Total Loan Amount], SAMEPERIODLASTYEAR(dim_date[date]))
)
