# ABC Bank — Self-Service Customer Lookup Kiosk

A small Flask app that lets a bank customer scan their ID (Aadhaar, PAN, or Driving
License) at a kiosk and instantly see their account balance, deposits, loans, gold
holdings, cards, and recent transactions — no counter, no waiting in line, no manual
account-number lookup.

Identity reading is done by a self-hosted **Qwen2.5-VL** vision-language model served
via **Ollama** on a remote GPU server. No cloud AI APIs (OpenAI, Anthropic, etc.) are
used anywhere in this project.

This project reuses the exact `ocr_extract.py` module from the AOF eKYC project, and
seeds its database from the same 5 fictional sample customers as
`Sample_Customer_Data.xlsx`.

---

## How it works

```
Customer                    Flask App                   Remote GPU Server
   |                            |                               |
   | 1. Scans ID at kiosk        |                               |
   |--------------------------->|                               |
   |                            | 2. Sends image + prompt        |
   |                            |------------------------------>|
   |                            |                        Qwen2.5-VL reads name + DOB
   |                            | 3. Returns extracted JSON       |
   |                            |<------------------------------|
   |                            | 4. Matches name+DOB against     |
   |                            |    seeded Customer table        |
   | 5. Lands on dashboard       |                               |
   |<---------------------------|                               |
```

If the scan fails, or no matching customer is found, the app fails closed — it never
guesses and never shows the wrong person's data. The customer is told to try again or
see a counter instead.

---

## Features

- **One-step lookup**: scan ID → matched dashboard, no typing an account number
- **Identity match on name + DOB together** (not name alone, since two people can
  share a first name)
- **Consolidated dashboard**: accounts & balances, FD/RD deposits, gold loans/deposits,
  loans (with an eligibility note), cards, other investments, interest & charges, and
  the last 5 transactions — all in one view
- **Adapts per customer**: a section only renders if that customer actually has data
  in it — no empty "Loans" box for someone with no loans
- **Internal data never modeled**: compliance/risk fields (PEP status, sanctions
  screening, dormancy flags) aren't just hidden in the template — they're not even
  queried, because there's no `Compliance` model in this app at all

---

## Project structure

```
customer_lookup/
├── app.py              # Routes: home, ID scan/lookup, dashboard
├── config.py            # DB, upload, and Ollama connection settings
├── extensions.py         # Shared SQLAlchemy db object
├── models.py              # 10 tables (Customer + 9 linked product tables), keyed by CIF
├── ocr_extract.py         # Talks to Qwen2.5-VL via Ollama (same module as the AOF project)
├── seed_data.py            # Loads the 5 fictional sample customers into the DB
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── lookup.html
│   └── dashboard.html
├── static/css/style.css
└── uploads/                 # Saved ID scan images (auto-created)
```

---

## Setup & running

### 1. On the remote GPU server (where Qwen2.5-VL runs)

```bash
ollama pull qwen2.5vl:7b
OLLAMA_HOST=0.0.0.0 ollama serve
```

Ollama only listens on `127.0.0.1` by default — `OLLAMA_HOST=0.0.0.0` is required for
this app (running elsewhere) to reach it.

**Security note:** Ollama has no built-in authentication. Don't expose port `11434`
to the open internet — restrict it to known IPs via firewall/security group, or tunnel
over SSH:
```bash
ssh -L 11434:localhost:11434 user@remote-gpu-server
```

### 2. On the machine running this Flask app

```bash
cd customer_lookup
pip install -r requirements.txt
```

Edit `config.py` and point `OLLAMA_HOST` at your server:
```python
OLLAMA_HOST = "http://203.0.113.10:11434"   # or http://localhost:11434 if tunneling
```

### 3. Seed the database (run once)

```bash
python seed_data.py
```
Expected output: `Seeded 5 customers and all related records.`

### 4. Run the app

```bash
python app.py
```

Open `http://localhost:5002`.

### 5. Try it

Click **"Scan My ID"** → pick a document type → upload a photo. Since these are
fictional customers with no real ID photos, the simplest way to test is a plain image
containing one of the seeded names + DOB as text (e.g. "Priya Nair, DOB 22/04/1988") —
Qwen2.5-VL just needs to read those two fields off whatever image it's given.

Quick connectivity check if scanning seems to hang or fail outright:
```bash
curl http://<your-remote-gpu-server-ip>:11434/api/tags
```
If that doesn't respond, it's a network/firewall issue between this machine and the
GPU server — not a bug in the app.

---

## The 5 sample customers

| Customer | DOB | Has |
|---|---|---|
| Priya Nair | 22/04/1988 | Savings account, FD, RD, PPF, debit card |
| Arjun Mehta | 09/11/1985 | Current + savings account, business loan, credit card, demat |
| Sunita Iyer | 30/06/1979 | Savings account, FD, **gold loan** |
| Vikram Desai | 17/02/1992 | Salary account, **home loan**, 2 cards, NPS, locker |
| Fatima Sheikh | 05/12/1995 | Savings account, RD, **gold monetization deposit**, mutual fund |

Deliberately uneven on purpose — every customer has accounts, but not every customer
has every product, so the dashboard's conditional sections actually get exercised.

---

## Identity matching logic

`app.py` matches on **full name (case-insensitive) AND date of birth together**:

```python
match = Customer.query.filter(
    db.func.lower(Customer.full_name) == scanned_name,
    Customer.dob == scanned_dob,
).first()
```

This is a reasonable proxy for "this is genuinely the person who just scanned their
ID" without requiring a PIN, login, or second factor — appropriate for a kiosk demo,
but worth strengthening (e.g. requiring the registered mobile number too, or a PIN
sent via SMS) before this pattern is used with real customer data in production.

---

## What's been tested vs. what to verify yourself

Tested end-to-end with mocked Ollama responses:
- ✅ Successful scan + match → full dashboard renders with correct data
- ✅ Successful scan, no matching customer → graceful "see a counter" message
- ✅ Scan/extraction failure (simulated Ollama unreachable) → graceful fallback message
- ✅ Conditional sections render correctly per customer (gold loan shows for Sunita,
  not for others; loans section shows for Arjun/Vikram, not for Priya/Fatima/Sunita)
- ✅ No compliance/internal data appears anywhere in the rendered dashboard

**Not tested (can't be, from this environment):**
- Actual extraction accuracy of `qwen2.5vl:7b` reading a real or sample ID photo —
  that depends on your real remote server and real images
- Network latency/reliability between your Flask app and the remote GPU server

---

## Possible extensions

- Require a second factor (registered mobile + OTP) before showing the dashboard
- Log every lookup attempt (matched or not) for audit/fraud-monitoring purposes
- Add a "this isn't me" button on the dashboard that flags the session for review
- Auto-clear/timeout the dashboard view after a short idle period (kiosk screens are
  public — someone walking away shouldn't leave their balance on screen indefinitely)
