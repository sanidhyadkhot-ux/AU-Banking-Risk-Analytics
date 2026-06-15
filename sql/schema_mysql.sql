
-- AU Banking Risk Analytics 2026 | MySQL schema
CREATE DATABASE IF NOT EXISTS au_banking_risk;
USE au_banking_risk;

CREATE TABLE dim_client (
  client_id VARCHAR(20) PRIMARY KEY,
  age INT,
  gender VARCHAR(10),
  state VARCHAR(10),
  occupation VARCHAR(50),
  income DECIMAL(12,2),
  income_band VARCHAR(20),
  join_year INT,
  nationality VARCHAR(50),
  marital VARCHAR(30),
  education VARCHAR(60)
);

CREATE TABLE dim_loan_product (
  product_id VARCHAR(10) PRIMARY KEY,
  product_type VARCHAR(40),
  base_interest_rate DECIMAL(5,2)
);

CREATE TABLE dim_advisor (
  advisor_id VARCHAR(10) PRIMARY KEY,
  advisor_name VARCHAR(80),
  branch VARCHAR(80),
  performance_rating VARCHAR(5)
);

CREATE TABLE dim_date (
  date DATE PRIMARY KEY,
  date_id INT,
  year INT,
  month INT,
  quarter VARCHAR(5),
  financial_year VARCHAR(10)
);

CREATE TABLE fact_banking_relationship (
  client_id VARCHAR(20),
  product_id VARCHAR(10),
  advisor_id VARCHAR(10),
  date DATE,
  bank_division VARCHAR(40),
  loan_amount DECIMAL(14,2),
  deposit_amount DECIMAL(14,2),
  checking_balance DECIMAL(14,2),
  saving_balance DECIMAL(14,2),
  credit_score INT,
  default_flag INT,
  risk_score DECIMAL(5,2),
  risk_segment VARCHAR(20),
  debt_to_income_ratio DECIMAL(8,2),
  loan_to_deposit_ratio DECIMAL(8,2),
  FOREIGN KEY (client_id) REFERENCES dim_client(client_id),
  FOREIGN KEY (product_id) REFERENCES dim_loan_product(product_id),
  FOREIGN KEY (advisor_id) REFERENCES dim_advisor(advisor_id),
  FOREIGN KEY (date) REFERENCES dim_date(date)
);
