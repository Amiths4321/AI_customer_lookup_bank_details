import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from config import Config
from extensions import db
from models import (Customer, Account, Deposit, GoldProduct, Loan, Card,
                     Investment, Transaction, InterestCharge, DigitalBanking)
from ocr_extract import extract_document

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/lookup", methods=["GET", "POST"])
def lookup():
    if request.method == "POST":
        doc_type = request.form.get("document_type")
        doc_file = request.files.get("document_image")

        if doc_type not in ("Aadhaar", "PAN", "Driving License"):
            flash("Please select a document type.")
            return redirect(url_for("lookup"))

        if not doc_file or not doc_file.filename or not allowed_file(doc_file.filename):
            flash("Please upload a valid image file (png, jpg, jpeg).")
            return redirect(url_for("lookup"))

        fname = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{doc_file.filename}")
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
        doc_file.save(save_path)

        success, data, raw_text, error_message = extract_document(
            save_path, doc_type,
            app.config["OLLAMA_HOST"], app.config["OLLAMA_MODEL"], app.config["OLLAMA_TIMEOUT_SECONDS"],
        )

        if not success:
            flash(f"Couldn't scan your document ({error_message}). Please ask a staff member for help.")
            return redirect(url_for("lookup"))

        scanned_name = (data.get("full_name") or "").strip().lower()
        scanned_dob = (data.get("dob") or "").strip()

        match = Customer.query.filter(
            db.func.lower(Customer.full_name) == scanned_name,
            Customer.dob == scanned_dob,
        ).first()

        if not match:
            flash("We couldn't find a matching record. Please proceed to a counter for assistance.")
            return redirect(url_for("lookup"))

        return redirect(url_for("dashboard", cif=match.cif))

    return render_template("lookup.html")


@app.route("/dashboard/<cif>")
def dashboard(cif):
    customer = Customer.query.get_or_404(cif)
    accounts = Account.query.filter_by(cif=cif).all()
    deposits = Deposit.query.filter_by(cif=cif).all()
    gold = GoldProduct.query.filter_by(cif=cif).all()
    loans = Loan.query.filter_by(cif=cif).all()
    cards = Card.query.filter_by(cif=cif).all()
    investments = Investment.query.filter_by(cif=cif).all()
    transactions = Transaction.query.filter_by(cif=cif).order_by(Transaction.id.desc()).limit(5).all()
    interest = InterestCharge.query.filter_by(cif=cif).first()
    digital = DigitalBanking.query.filter_by(cif=cif).first()

    return render_template(
        "dashboard.html", customer=customer, accounts=accounts, deposits=deposits,
        gold=gold, loans=loans, cards=cards, investments=investments,
        transactions=transactions, interest=interest, digital=digital,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)