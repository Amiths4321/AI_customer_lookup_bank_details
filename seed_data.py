"""
Run this once after the database tables are created to load the 5 sample
customers (same fictional dataset as Sample_Customer_Data.xlsx) into the DB.

    python seed_data.py
"""
from app import app
from extensions import db
from models import (Customer, Account, Deposit, GoldProduct, Loan, Card,
                     Investment, Transaction, InterestCharge, DigitalBanking)


def seed():
    db.drop_all()
    db.create_all()

    customers = [
        Customer(cif="CIF1023456001", full_name="Priya Nair", dob="22/04/1988", gender="Female",
                 pan="BNZPN4521K", aadhaar_masked="XXXX XXXX 7734", mobile="9821345610",
                 email="priya.nair88@example.com",
                 address="14 Lake View Apartments, Powai, Mumbai 400076",
                 occupation="Salaried — IT Professional", annual_income=950000, marital_status="Married",
                 nominee_name="Anand Nair", nominee_relation="Spouse", customer_since="18-Jan-2016",
                 home_branch="Powai Branch", ifsc="BRGT0001012", kyc_status="Verified, 05-Feb-2024"),
        Customer(cif="CIF1023456002", full_name="Arjun Mehta", dob="09/11/1985", gender="Male",
                 pan="ALWPM7789C", aadhaar_masked="XXXX XXXX 2210", mobile="9876512340",
                 email="arjun.mehta85@example.com",
                 address="B-12 Sahyadri Society, Kothrud, Pune 411038",
                 occupation="Self-employed — Business Owner", annual_income=1450000, marital_status="Married",
                 nominee_name="Kavita Mehta", nominee_relation="Spouse", customer_since="22-Jul-2012",
                 home_branch="Kothrud Branch", ifsc="BRGT0002045", kyc_status="Verified, 11-Nov-2023"),
        Customer(cif="CIF1023456003", full_name="Sunita Iyer", dob="30/06/1979", gender="Female",
                 pan="AOPPI3345R", aadhaar_masked="XXXX XXXX 9087", mobile="9912233445",
                 email="sunita.iyer79@example.com",
                 address="27 Matunga Cross Road, Matunga, Mumbai 400019",
                 occupation="Homemaker", annual_income=0, marital_status="Widowed",
                 nominee_name="Karthik Iyer", nominee_relation="Son", customer_since="03-Mar-2009",
                 home_branch="Matunga Branch", ifsc="BRGT0001233", kyc_status="Verified, 14-Dec-2023"),
        Customer(cif="CIF1023456004", full_name="Vikram Desai", dob="17/02/1992", gender="Male",
                 pan="CKQPD9912H", aadhaar_masked="XXXX XXXX 5561", mobile="9988776655",
                 email="vikram.desai92@example.com",
                 address="402 Hill Crest CHS, Ghodbunder Road, Thane 400607",
                 occupation="Salaried — Bank Employee", annual_income=1100000, marital_status="Single",
                 nominee_name="Meena Desai", nominee_relation="Mother", customer_since="09-Sep-2019",
                 home_branch="Thane West Branch", ifsc="BRGT0003781", kyc_status="Verified, 02-Jan-2026"),
        Customer(cif="CIF1023456005", full_name="Fatima Sheikh", dob="05/12/1995", gender="Female",
                 pan="DLEPS6678M", aadhaar_masked="XXXX XXXX 3349", mobile="9001122334",
                 email="fatima.sheikh95@example.com",
                 address="18 Crescent Apartments, Bandra West, Mumbai 400050",
                 occupation="Salaried — Marketing Executive", annual_income=780000, marital_status="Single",
                 nominee_name="Imran Sheikh", nominee_relation="Father", customer_since="26-Jun-2021",
                 home_branch="Bandra Branch", ifsc="BRGT0001577", kyc_status="Verified, 19-Mar-2024"),
    ]
    db.session.add_all(customers)

    accounts = [
        Account(cif="CIF1023456001", account_number="502100123456701", account_type="Savings",
                opening_date="18-Jan-2016", status="Active", mode_of_operation="Single",
                current_balance=184250, available_balance=184250, min_balance_req=10000, amb=142300),
        Account(cif="CIF1023456002", account_number="502100123456702", account_type="Current",
                opening_date="22-Jul-2012", status="Active", mode_of_operation="Single",
                current_balance=612400, available_balance=612400, min_balance_req=25000, amb=540000),
        Account(cif="CIF1023456002", account_number="502100123456709", account_type="Savings",
                opening_date="05-Jan-2018", status="Active", mode_of_operation="Joint (Either-or-Survivor)",
                current_balance=95000, available_balance=92000, min_balance_req=10000, amb=88000),
        Account(cif="CIF1023456003", account_number="502100123456703", account_type="Savings",
                opening_date="03-Mar-2009", status="Active", mode_of_operation="Single",
                current_balance=326800, available_balance=326800, min_balance_req=5000, amb=310500),
        Account(cif="CIF1023456004", account_number="502100123456704", account_type="Salary",
                opening_date="09-Sep-2019", status="Active", mode_of_operation="Single",
                current_balance=78650, available_balance=78650, min_balance_req=0, amb=65200),
        Account(cif="CIF1023456005", account_number="502100123456705", account_type="Savings",
                opening_date="26-Jun-2021", status="Active", mode_of_operation="Single",
                current_balance=54300, available_balance=54300, min_balance_req=10000, amb=48900),
    ]
    db.session.add_all(accounts)

    deposits = [
        Deposit(cif="CIF1023456001", deposit_account_no="FD7700123401", deposit_type="Fixed Deposit",
                principal_installment=200000, interest_rate="7.25%", tenure="2 years",
                booking_date="10-Jun-2024", maturity_date="10-Jun-2026", maturity_value=230500,
                payout_option="Cumulative", auto_renewal="Yes"),
        Deposit(cif="CIF1023456001", deposit_account_no="RD7700123402", deposit_type="Recurring Deposit",
                principal_installment=5000, interest_rate="6.75%", tenure="3 years",
                booking_date="01-Jan-2025", maturity_date="01-Jan-2028", maturity_value=195400,
                payout_option="Cumulative", auto_renewal="No"),
        Deposit(cif="CIF1023456003", deposit_account_no="FD7700123403", deposit_type="Fixed Deposit",
                principal_installment=500000, interest_rate="7.50%", tenure="1 year",
                booking_date="14-Dec-2025", maturity_date="14-Dec-2026", maturity_value=537500,
                payout_option="Monthly Payout", auto_renewal="Yes"),
        Deposit(cif="CIF1023456005", deposit_account_no="RD7700123404", deposit_type="Recurring Deposit",
                principal_installment=3000, interest_rate="6.75%", tenure="1 year",
                booking_date="01-Apr-2025", maturity_date="01-Apr-2026", maturity_value=37300,
                payout_option="Cumulative", auto_renewal="No"),
    ]
    db.session.add_all(deposits)

    gold = [
        GoldProduct(cif="CIF1023456003", gold_account_no="GL7700123401", product_type="Gold Loan",
                    gold_weight_purity="45g, 22 karat", valuation=315000, loan_deposit_amount=220500,
                    rate_detail="LTV 70%", interest_rate="9.50% p.a.", tenure="12 months (bullet)",
                    outstanding_balance=180000, status="Active"),
        GoldProduct(cif="CIF1023456005", gold_account_no="GM7700123402",
                    product_type="Gold Monetization Scheme Deposit", gold_weight_purity="50g, 22 karat",
                    valuation=None, loan_deposit_amount=50, rate_detail="Medium Term Govt Deposit",
                    interest_rate="2.25% p.a. (paid in gold)", tenure="5 years",
                    outstanding_balance=None, status="Active"),
    ]
    db.session.add_all(gold)

    loans = [
        Loan(cif="CIF1023456002", loan_account_no="LN7700123401", loan_type="Business Loan",
             sanctioned_amount=1500000, disbursed_amount=1500000, interest_rate="11.25% p.a. (floating)",
             tenure="5 years", emi=32700, outstanding_principal=980000, next_emi_due="05th of every month",
             status="Active", collateral="Hypothecation of business assets",
             co_applicant="Kavita Mehta (Spouse)", credit_score=728,
             eligibility_note="FOIR 32% — eligible for ~₹3L additional top-up"),
        Loan(cif="CIF1023456004", loan_account_no="LN7700123402", loan_type="Home Loan",
             sanctioned_amount=3500000, disbursed_amount=3500000,
             interest_rate="8.65% p.a. (floating, repo-linked)", tenure="20 years", emi=30500,
             outstanding_principal=3240000, next_emi_due="05th of every month", status="Active",
             collateral="Property title — Flat 402, Hill Crest CHS", co_applicant="—", credit_score=742,
             eligibility_note="FOIR 38% — limited additional eligibility"),
    ]
    db.session.add_all(loans)

    cards = [
        Card(cif="CIF1023456001", card_number_masked="XXXX XXXX XXXX 4521", card_type="Debit Card",
             variant="Platinum Debit", credit_limit=None, outstanding=None, billing_cycle="—",
             due_date="—", reward_points=None),
        Card(cif="CIF1023456002", card_number_masked="XXXX XXXX XXXX 8890", card_type="Credit Card",
             variant="Business Rewards", credit_limit=500000, outstanding=184000,
             billing_cycle="1st–end of month", due_date="20th", reward_points=12400),
        Card(cif="CIF1023456004", card_number_masked="XXXX XXXX XXXX 1187", card_type="Debit Card",
             variant="Classic Debit", credit_limit=None, outstanding=None, billing_cycle="—",
             due_date="—", reward_points=None),
        Card(cif="CIF1023456004", card_number_masked="XXXX XXXX XXXX 6643", card_type="Credit Card",
             variant="Cashback Card", credit_limit=150000, outstanding=18400,
             billing_cycle="1st–end of month", due_date="20th", reward_points=4250),
    ]
    db.session.add_all(cards)

    investments = [
        Investment(cif="CIF1023456001", product="PPF", account_folio_no="PPF7700123401",
                   balance_summary="₹4,12,000",
                   details="Opened FY 2016-17, ₹1,00,000 contributed FY 2025-26"),
        Investment(cif="CIF1023456002", product="Demat Account", account_folio_no="IN30012345678901",
                   balance_summary="120 shares across 6 scrips",
                   details="Linked to trading account via partner broker"),
        Investment(cif="CIF1023456004", product="NPS", account_folio_no="PRAN110045678901",
                   balance_summary="₹2,85,000", details="Tier I, Equity allocation 50%"),
        Investment(cif="CIF1023456004", product="Locker", account_folio_no="LKR-B-204",
                   balance_summary="Size: Medium",
                   details="Annual rent ₹3,000, Nominee: Meena Desai"),
        Investment(cif="CIF1023456005", product="Mutual Fund (via bank)", account_folio_no="MF7700998812",
                   balance_summary="₹62,000", details="SIP ₹3,000/month across 2 schemes"),
    ]
    db.session.add_all(investments)

    transactions = [
        Transaction(cif="CIF1023456001", account_number="502100123456701", txn_date="12-Jun-2026",
                    narration="UPI/RAHULSHARMA/RENT", txn_type="Debit", amount=18000, running_balance=184250),
        Transaction(cif="CIF1023456001", account_number="502100123456701", txn_date="10-Jun-2026",
                    narration="SALARY CREDIT - INFOTECH SOLUTIONS", txn_type="Credit", amount=95000,
                    running_balance=202250),
        Transaction(cif="CIF1023456001", account_number="502100123456701", txn_date="05-Jun-2026",
                    narration="NEFT/ELECTRICITY BOARD", txn_type="Debit", amount=2400, running_balance=107250),
        Transaction(cif="CIF1023456002", account_number="502100123456702", txn_date="15-Jun-2026",
                    narration="NEFT/SUPPLIER PAYMENT/RAWMAT", txn_type="Debit", amount=220000,
                    running_balance=612400),
        Transaction(cif="CIF1023456002", account_number="502100123456702", txn_date="14-Jun-2026",
                    narration="CHEQUE DEPOSIT - CLIENT INVOICE", txn_type="Credit", amount=350000,
                    running_balance=832400),
        Transaction(cif="CIF1023456004", account_number="502100123456704", txn_date="05-Jun-2026",
                    narration="EMI - HOME LOAN LN7700123402", txn_type="Debit", amount=30500,
                    running_balance=78650),
        Transaction(cif="CIF1023456004", account_number="502100123456704", txn_date="01-Jun-2026",
                    narration="SALARY CREDIT - BRIGHTBANK PAYROLL", txn_type="Credit", amount=92000,
                    running_balance=109150),
    ]
    db.session.add_all(transactions)

    interest_charges = [
        InterestCharge(cif="CIF1023456001", period="2025-26", interest_earned=14800, interest_charged=0,
                       tds_deducted=0, form15g_status="Not Required (below threshold)",
                       maintenance_charges=0, penalty_charges=0),
        InterestCharge(cif="CIF1023456002", period="2025-26", interest_earned=6200, interest_charged=168900,
                       tds_deducted=0, form15g_status="Not Submitted", maintenance_charges=590,
                       penalty_charges=0),
        InterestCharge(cif="CIF1023456003", period="2025-26", interest_earned=38200, interest_charged=0,
                       tds_deducted=3820, form15g_status="Submitted (Form 15H — Senior Citizen)",
                       maintenance_charges=0, penalty_charges=0),
        InterestCharge(cif="CIF1023456004", period="2025-26", interest_earned=3100, interest_charged=271400,
                       tds_deducted=0, form15g_status="Not Submitted", maintenance_charges=0,
                       penalty_charges=590),
        InterestCharge(cif="CIF1023456005", period="2025-26", interest_earned=1900, interest_charged=0,
                       tds_deducted=0, form15g_status="Not Required (below threshold)",
                       maintenance_charges=0, penalty_charges=0),
    ]
    db.session.add_all(interest_charges)

    digital = [
        DigitalBanking(cif="CIF1023456001", net_banking_user_id="pnair88", net_banking_status="Active",
                       mobile_banking_status="Active", alert_preferences="SMS + Email",
                       statement_preference="e-Statement", upi_handles="priyanair88@brightbank"),
        DigitalBanking(cif="CIF1023456002", net_banking_user_id="amehta85biz", net_banking_status="Active",
                       mobile_banking_status="Active", alert_preferences="SMS + Email",
                       statement_preference="e-Statement", upi_handles="arjunmehta@brightbank"),
        DigitalBanking(cif="CIF1023456003", net_banking_user_id="siyer79", net_banking_status="Active",
                       mobile_banking_status="Inactive", alert_preferences="SMS only",
                       statement_preference="Physical", upi_handles="—"),
        DigitalBanking(cif="CIF1023456004", net_banking_user_id="vdesai92", net_banking_status="Active",
                       mobile_banking_status="Active", alert_preferences="SMS + Email",
                       statement_preference="e-Statement", upi_handles="vikramdesai92@brightbank"),
        DigitalBanking(cif="CIF1023456005", net_banking_user_id="fsheikh95", net_banking_status="Active",
                       mobile_banking_status="Active", alert_preferences="Email only",
                       statement_preference="e-Statement", upi_handles="fatimasheikh95@brightbank"),
    ]
    db.session.add_all(digital)

    db.session.commit()
    print(f"Seeded {len(customers)} customers and all related records.")


if __name__ == "__main__":
    with app.app_context():
        seed()