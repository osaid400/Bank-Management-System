import json
import hashlib
from pathlib import Path
from datetime import datetime
from src.models import BankAccount

class BankManager:

    def __init__(self, filename="data/accounts.json"):
        self.filename = Path(filename)
        self.accounts = []
        self._receipt_counter = 0
        self.load_accounts()

        if not self.accounts and not self.filename.exists():
            self.accounts = [
                BankAccount("Ali", 3011, 15000, "1234", "Savings"),
                BankAccount("Abdullah", 3012, 23500, "1234", "Current"),
                BankAccount("Ahmed", 3013, 23500, "1234", "Savings"),
                BankAccount("Zohaib", 3014, 55500, "1234", "Current"),
                BankAccount("Fabiha", 3015, 13500, "1234", "Savings"),
            ]
            self.save_accounts()

    def get_next_account_number(self):
        if not self.accounts:
            return 3011
        return max(acc.account_number for acc in self.accounts) + 1

    def admin_login(self, username, password):
        admin_user_hash = hashlib.sha256("admin".encode()).hexdigest()
        admin_pass_hash = hashlib.sha256("12345".encode()).hexdigest()
        
        input_user_hash = hashlib.sha256(username.strip().encode()).hexdigest()
        input_pass_hash = hashlib.sha256(password.strip().encode()).hexdigest()
        
        return input_user_hash == admin_user_hash and input_pass_hash == admin_pass_hash

    def generate_bank_report(self):
        total_deposits = sum(acc.balance for acc in self.accounts)
        total_approved_loans = sum(acc.loan_balance for acc in self.accounts)
        total_pending_loans = sum(acc.pending_loan for acc in self.accounts)
        pending_checkbooks = sum(1 for acc in self.accounts if acc.checkbook_status == "Pending")
        frozen_accounts = sum(1 for acc in self.accounts if not acc.is_active)
        total_transactions = sum(len(acc._transactions) for acc in self.accounts)

        return {
            "Total Customers": len(self.accounts),
            "Active Accounts": len(self.accounts) - frozen_accounts,
            "Frozen Accounts": frozen_accounts,
            "Total Bank Deposits": total_deposits,
            "Total Approved Loans": total_approved_loans,
            "Total Pending Loans Amount": total_pending_loans,
            "Pending Checkbook Requests": pending_checkbooks,
            "Total System Transactions": total_transactions
        }

    def load_accounts(self):
        if self.filename.exists():
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.accounts = [BankAccount.from_dict(item) for item in data]
            except (json.JSONDecodeError, ValueError, OSError):
                self.accounts = []

    def save_accounts(self):
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filename, "w", encoding="utf-8") as file:
            data = [acc.to_dict() for acc in self.accounts]
            json.dump(data, file, indent=4)

    def toggle_account_status(self, account):
        account.is_active = not account.is_active
        status_str = "Active" if account.is_active else "Frozen"
        account.record_transaction(f"Account Status Changed: {status_str}", 0)
        self.save_accounts()
        return account.is_active

    def approve_loan(self, account):
        if account.pending_loan <= 0:
            raise ValueError("No pending loan request found for this account.")
        
        loan_amt = account.pending_loan
        account.loan_balance = loan_amt
        account.receive_loan_disbursement(loan_amt)
        account.pending_loan = 0.0
        account.record_transaction("Loan Approved", loan_amt)
        self.save_accounts()

    def reject_loan(self, account):
        account.reject_loan()
        self.save_accounts()

    def approve_checkbook(self, account):
        if account.checkbook_status != "Pending":
            raise ValueError("No pending checkbook request found for this account.")
        account.checkbook_status = "Approved"
        account.record_transaction("Checkbook Approved", 0)
        self.save_accounts()

    def reject_checkbook(self, account):
        account.reject_checkbook()
        self.save_accounts()

    def find_account(self, account_number):
        try:
            acc_num = int(account_number)
            return next((acc for acc in self.accounts if acc.account_number == acc_num), None)
        except ValueError:
            return None

    def search_accounts(self, query):
        normalized = str(query).strip().lower()
        return [acc for acc in self.accounts if normalized == str(acc.account_number) or normalized in acc.name.lower()]

    def apply_monthly_interest_to_all(self):
        count = 0
        for acc in self.accounts:
            if acc.account_type == "Savings" and acc.balance > 0 and acc.is_active:
                acc.calculate_interest()
                count += 1
        self.save_accounts()
        return count

    def transfer_money(self, sender_account, receiver_account, amount):
        sender_account.check_active_status()
        receiver_account.check_active_status()

        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero!")
        if amount > 100000:
            raise ValueError("Single transfer limit exceeded! (Max Rs. 100,000)")
        if sender_account.account_number == receiver_account.account_number:
            raise ValueError("You cannot transfer money to your own account.")

        sender_account.withdraw(amount)
        receiver_account.deposit(amount)
        
        sender_account._transactions[-1]["Type"] = "Transfer Sent"
        receiver_account._transactions[-1]["Type"] = "Transfer Received"

        self.save_accounts()
        return True

    def open_account(self, name, initial_deposit, pin, account_type="Savings"):
        account_number = self.get_next_account_number()
        
        acc_type_clean = account_type.strip().capitalize()
        if acc_type_clean not in ["Savings", "Current"]:
            raise ValueError("Account type must be either 'Savings' or 'Current'.")

        if acc_type_clean == "Savings" and initial_deposit < 2000:
            raise ValueError("Minimum initial deposit for Savings Account is Rs. 2,000.")
        elif acc_type_clean == "Current" and initial_deposit < 1000:
            raise ValueError("Minimum initial deposit for Current Account is Rs. 1,000.")

        if not str(pin).strip().isdigit() or len(str(pin).strip()) != 4:
            raise ValueError("PIN must be exactly 4 digits.")
            
        new_acc = BankAccount(name, account_number, initial_deposit, pin, account_type=acc_type_clean)
        self.accounts.append(new_acc)
        self.save_accounts()
        return new_acc

    def close_account(self, account):
        if account.balance != 0 or account.loan_balance != 0:
            raise ValueError("Account must have zero balance and no active loan to close.")
        if account.pending_loan > 0:
            raise ValueError("Cannot close account with a pending loan request.")
        if account.checkbook_status == "Pending":
            raise ValueError("Cannot close account with a pending checkbook request.")

        self.accounts.remove(account)
        self.save_accounts()

    def generate_receipt(self, account, transaction_type, amount, description="", subfolder="general"):
        receipts_dir = Path("receipts") / subfolder
        receipts_dir.mkdir(parents=True, exist_ok=True)
        
        self._receipt_counter += 1
        file_name = f"{account.account_number}_TXN{self._receipt_counter:04d}.txt"
        receipt_path = receipts_dir / file_name

        lines = [
            "=" * 60,
            "BANK MANAGEMENT SYSTEM - RECEIPT".center(60),
            "=" * 60,
            f"Account Holder : {account.name}",
            f"Account Number : {account.account_number}",
            f"Account Type   : {account.account_type}",
            f"Date           : {datetime.now().strftime('%Y-%m-%d')}",
            f"Time           : {datetime.now().strftime('%H:%M:%S')}",
            f"Transaction    : {transaction_type}",
            f"Amount         : Rs. {float(amount):,.2f}",
            f"Description    : {description or 'N/A'}",
            f"Current Balance: Rs. {account.balance:,.2f}",
            "=" * 60,
        ]
        receipt_path.write_text("\n".join(lines), encoding="utf-8")
        return receipt_path