# Bank Management System

A console-based Bank Management System built with Python using Object-Oriented Programming (OOP) principles. Unlike a simple ATM simulator, this project models real banking operations — account opening, loans, checkbooks, interest, and admin oversight — with secure PIN hashing, JSON-based data persistence, and a modular package structure.

---

## Features

* **Admin Panel:**
  * Secure Admin Login
  * Open New Account (auto-assigned account number, Savings/Current)
  * Close Account (blocked if balance, loan, or pending requests exist)
  * Freeze / Unfreeze Account
  * Manage Loan Requests (Approve / Reject)
  * Manage Checkbook Requests (Approve / Reject)
  * View Complete Bank Report (deposits, loans, transactions, per-account overview)
  * Apply Monthly Interest to All Savings Accounts

* **Customer System:**
  * Login (Account Number + PIN)
  * Check Balance (with account type, status, and pending requests shown)
  * Deposit / Withdraw Money
  * Change PIN
  * Cash Statement (last 30 days)
  * Mini Statement (last 5 transactions)
  * Transfer Money (with self-transfer and limit checks)
  * Apply for Loan / Return Loan
  * Request Checkbook

* **Data & Security Features:**
  * SHA-256 PIN Hashing (no plaintext PINs stored)
  * Persistent JSON Storage with backward-compatible loading (handles both legacy and current data formats)
  * Auto-generated Transaction Receipts (`.txt`, saved under `receipts/`)
  * Per-transaction limit (Rs. 100,000) and daily withdrawal limit (Rs. 200,000)
  * Savings minimum balance (Rs. 2,000) vs. Current account overdraft allowance (Rs. 50,000)
  * Account Freeze/Unfreeze (frozen accounts blocked from all transactions)
  * Full transaction history logging with date and time
  * Input validation and exception handling throughout

---

## Technologies Used

* **Python 3** (Object-Oriented Programming)
* **JSON Module** (Data persistence)
* **hashlib** (SHA-256 PIN hashing)
* **pathlib** (File and directory handling)
* **Datetime Module** (Timestamps, interest cycles, statement filtering)

---

## Project Structure

```text
Bank-Management-System/
│
├── data/
│   └── accounts.json          # Persistent JSON account records (gitignored)
│
├── receipts/                  # Auto-generated transaction receipts (gitignored)
│   ├── general/
│   ├── sent/
│   └── received/
│
├── src/                       # Source code package
│   ├── __init__.py
│   ├── models.py               # BankAccount class — data, validation, and account-level operations
│   ├── manager.py               # BankManager class — persistence, admin operations, multi-account logic
│   └── UI.py                    # CLI menus and display formatting
│
├── .gitignore                 # Excludes __pycache__, receipts, and local data
├── main.py                    # Application entry point
└── README.md
```

> **Note:** `data/accounts.json` is created automatically on first run with sample accounts. It stores account records and full transaction history locally, and is excluded from the repository via `.gitignore`.

---

## How to Run

Clone the repository

```bash
git clone https://github.com/osaid400/Bank-Management-System.git
```

Move into the project folder

```bash
cd Bank-Management-System
```

Run the program

```bash
python main.py
```

---

## Example Outputs

### Main Menu

```text
============================================================
              WELCOME TO BANK MANAGEMENT SYSTEM
============================================================
1. Customer Login
2. Admin Login
0. Exit
------------------------------------------------------------
```

### Customer Login & Menu

```text
Enter Account Number: 3012
Enter 4-digit PIN: 4321

Login Successful!

============================================================
                     Welcome Back, Abdullah
============================================================
1. Check Balance
2. Deposit Money
3. Withdraw Money
4. Change Pin
5. Cash Statement (30 Days)
6. Transfer Money
7. Mini Statement
8. Request Checkbook
9. Apply Loan
10. Return Loan
11. Logout
0. Back to Main Menu
------------------------------------------------------------
```

### Apply for a Loan

```text
Enter choice: 9
Enter loan amount to apply for: 50000

Loan application of Rs. 50,000.00 submitted! Awaiting admin approval.
```

### Admin Panel — Manage Loan Requests

```text
--- PENDING LOAN REQUESTS ---
Account: 3012 | Name: Abdullah | Requested: Rs. 50,000.00

Enter account number to process: 3012
Type 'A' to Approve or 'R' to Reject: A

Loan of Rs. 50,000.00 approved for Abdullah.
```

### Admin Panel — Bank Report

```text
================================================================================
                 COMPREHENSIVE BANK FINANCIAL & ACTIVITY REPORT
================================================================================

------------------------------ GLOBAL FINANCIAL SUMMARY ------------------------
Total Customers                : 10
Active Accounts                : 9
Frozen Accounts                : 1
Total Bank Deposits            : Rs. 292,865.31
Total Approved Loans           : Rs. 50,000.00
Total Pending Loans Amount     : Rs. 0.00
Pending Checkbook Requests     : 1
Total System Transactions      : 34

------------------------- ALL CUSTOMER ACCOUNTS OVERVIEW ----------------------
Acc No   Name            Type       Status     Balance        Active Loan
--------------------------------------------------------------------------------
3011     Ali             Savings    ACTIVE     Rs.15,188      Rs.0
3012     Abdullah        Savings    ACTIVE     Rs.23,795      Rs.50,000
================================================================================
```

### Transaction Receipt (.txt output)

```text
============================================================
                BANK MANAGEMENT SYSTEM - RECEIPT
============================================================
Account Holder : Abdullah
Account Number : 3012
Account Type   : Savings
Date           : 2026-08-10
Time           : 09:47:17
Transaction    : Deposit
Amount         : Rs. 5,000.00
Description    : Cash Deposit
Current Balance: Rs. 28,795.00
============================================================
```

---

## Concepts Covered

* **Object-Oriented Programming (OOP):** Class design and encapsulation (`BankAccount`, `BankManager`), with private attributes (`__balance`, `__pin_hash`) accessed only through class-defined methods.
* **CRUD Operations:** Full account lifecycle — open, update (via transactions), close.
* **JSON Data Serialization:** Persistent, backward-compatible storage via `to_dict()` / `from_dict()`, handling both legacy and current data formats safely.
* **Security:** SHA-256 PIN hashing — no plaintext PINs are ever stored.
* **Business Logic & Validation:** Multi-step rules for withdrawals (per-transaction and daily limits, account-type-based minimum balance/overdraft), loans (eligibility, request-then-approve workflow), and account closure (blocked while pending requests exist).
* **Admin/Customer Role Separation:** Distinct menus and permissions — customers manage their own account; admins manage the whole bank.
* **Modules & Packages:** Code organized into a `src/` package (`models.py`, `manager.py`, `UI.py`), separating data, business logic, and presentation, with `main.py` as the entry point outside the package.
* **Defensive Programming:** Input validation and exception handling (`try`/`except`/`raise`) across all menus and operations.
* **Date & Time Handling:** Interest cycles, transaction timestamps, and 30-day statement filtering via `datetime`.

---

## How Loans & Checkbooks Work

* Customers **apply** for a loan or checkbook — this creates a *pending* request, it does not immediately grant anything.
* Admins review pending requests in the Admin Panel and **approve or reject** them.
* Only on approval does a loan disburse funds (via a dedicated `receive_loan_disbursement()` method that keeps the balance update inside the `BankAccount` class) or a checkbook get marked `Approved`.
* This mirrors how a real bank processes these requests — no self-service approval.

---

## Future Improvements

* Salted password hashing (current hashing is unsalted)
* Move admin credentials out of source code (environment variables or a config file)
* Three-attempt PIN lock system
* SQLite or PostgreSQL integration replacing JSON persistence
* RESTful API backend (FastAPI/Flask)
* Graphical User Interface (Tkinter)
* EMI-style scheduled loan repayment instead of manual lump-sum repayment
* Multi-currency support

---

## Learning Outcomes

This project helped me practice and solidify key software engineering concepts:

* **Encapsulation in practice:** Keeping balance and PIN mutations strictly inside `BankAccount`, and catching (then fixing) a real bug where manager code briefly reached into a private attribute directly from outside the class.
* **Designing approval workflows:** Separating "request" from "approval" for loans and checkbooks, closer to how real banking systems operate.
* **Backward-compatible persistence:** Writing a `from_dict()` that safely loads both older and newer JSON formats without crashing.
* **Business rule design:** Translating real-world constraints (overdraft limits, minimum balances, daily withdrawal caps) into validated code.
* **Modular project structure:** Splitting a single-file project into a `models` / `manager` / `UI` / `main` package, and understanding why each piece of logic belongs where it does.

---

## Author

**Muhammad Abdullah Farooq**

GitHub: [https://github.com/osaid400](https://github.com/osaid400)