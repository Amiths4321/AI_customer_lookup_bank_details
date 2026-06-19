from extensions import db


class Customer(db.Model):
    cif = db.Column(db.String(20), primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10))
    pan = db.Column(db.String(15))
    aadhaar_masked = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(300))
    occupation = db.Column(db.String(80))
    annual_income = db.Column(db.Float)
    marital_status = db.Column(db.String(20))
    nominee_name = db.Column(db.String(120))
    nominee_relation = db.Column(db.String(40))
    customer_since = db.Column(db.String(20))
    home_branch = db.Column(db.String(80))
    ifsc = db.Column(db.String(20))
    kyc_status = db.Column(db.String(80))


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), db.ForeignKey("customer.cif"), nullable=False)
    account_number = db.Column(db.String(30))
    account_type = db.Column(db.String(20))
    opening_date = db.Column(db.String(20))
    status = db.Column(db.String(20))
    mode_of_operation = db.Column(db.String(40))
    current_balance = db.Column(db.Float)
    available_balance = db.Column(db.Float)
    min_balance_req = db.Column(db.Float)
    amb = db.Column(db.Float)


class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), db.ForeignKey("customer.cif"), nullable=False)
    deposit_account_no = db.Column(db.String(30))
    deposit_type = db.Column(db.String(20))
    principal_installment = db.Column(db.Float)
    interest_rate = db.Column(db.String(20))
    tenure = db.Column(db.String(20))
    booking_date = db.Column(db.String(20))
    maturity_date = db.Column(db.String(20))
    maturity_value = db.Column(db.Float)
    payout_option = db.Column(db.String(30))
    auto_renewal = db.Column(db.String(10))


class GoldProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), db.ForeignKey("customer.cif"), nullable=False)
    gold_account_no = db.Column(db.String(30))
    product_type = db.Column(db.String(50))
    gold_weight_purity = db.Column(db.String(40))
    valuation = db.Column(db.Float)
    loan_deposit_amount = db.Column(db.Float)
    rate_detail = db.Column(db.String(40))
    interest_rate = db.Column(db.String(30))
    tenure = db.Column(db.String(30))
    outstanding_balance = db.Column(db.Float)
    status = db.Column(db.String(20))


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), db.ForeignKey("customer.cif"), nullable=False)
    loan_account_no = db.Column(db.String(30))
    loan_type = db.Column(db.String(30))
    sanctioned_amount = db.Column(db.Float)
    disbursed_amount = db.Column(db.Float)
    interest_rate = db.Column(db.String(40))
    tenure = db.Column(db.String(20))
    emi = db.Column(db.Float)
    outstanding_principal = db.Column(db.Float)
    next_emi_due = db.Column(db.String(30))
    status = db.Column(db.String(20))
    collateral = db.Column(db.String(200))
    co_applicant = db.Column(db.String(120))
    credit_score = db.Column(db.Integer)
    eligibility_note = db.Column(db.String(200))


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), db.ForeignKey("customer.cif"), nullable=False)
    card_number_masked = db.Column(db.String(30))
    card_type = db.Column(db.String(20))
    variant = db.Column(db.String(40))
    credit_limit = db.Column(db.Float)
    outstanding = db.Column(db.Float)
    billing_cycle = db.Column(db.String(40))
    due_date = db.Column(db.String(20))
    reward_points = db.Column(db.Integer)


class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), db.ForeignKey("customer.cif"), nullable=False)
    product = db.Column(db.String(40))
    account_folio_no = db.Column(db.String(40))
    balance_summary = db.Column(db.String(80))
    details = db.Column(db.String(200))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), db.ForeignKey("customer.cif"), nullable=False)
    account_number = db.Column(db.String(30))
    txn_date = db.Column(db.String(20))
    narration = db.Column(db.String(120))
    txn_type = db.Column(db.String(10))
    amount = db.Column(db.Float)
    running_balance = db.Column(db.Float)


class InterestCharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), db.ForeignKey("customer.cif"), nullable=False)
    period = db.Column(db.String(20))
    interest_earned = db.Column(db.Float)
    interest_charged = db.Column(db.Float)
    tds_deducted = db.Column(db.Float)
    form15g_status = db.Column(db.String(60))
    maintenance_charges = db.Column(db.Float)
    penalty_charges = db.Column(db.Float)


class DigitalBanking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), db.ForeignKey("customer.cif"), nullable=False)
    net_banking_user_id = db.Column(db.String(40))
    net_banking_status = db.Column(db.String(20))
    mobile_banking_status = db.Column(db.String(20))
    alert_preferences = db.Column(db.String(40))
    statement_preference = db.Column(db.String(20))
    upi_handles = db.Column(db.String(60))