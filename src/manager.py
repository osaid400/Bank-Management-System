# src/manager.py
import json
from pathlib import Path
from datetime import datetime
from src.models import BankAccount

class BankManager:

    def __init__(self, filename="data/accounts.json"):
        self.filename = Path(filename)
        self.accounts = []
        self._receipt_counter = 0
        self.load_accounts()

        if not self.accounts:
            self.accounts = [
                BankAccount("Ali", 3011, 15000, "1234"),
                BankAccount("Abdullah", 3012, 23500, "1234"),
                BankAccount("Ahmed", 3013, 23500, "1234"),
                BankAccount("Zohaib", 3014, 55500, "1234"),
                BankAccount("Fabiha", 3015, 13500, "1234"),
            ]
            self.save_accounts()

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

    def find_account(self, account_number):
        return next((acc for acc in self.accounts if acc.account_number == account_number), None)

    def transfer_money(self, sender_account, receiver_account, amount):
        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero!")
        if sender_account.account_number == receiver_account.account_number:
            raise ValueError("You cannot transfer money to your own account.")
        if sender_account.balance < amount:
            raise ValueError("Insufficient balance for this transfer.")

        sender_account.withdraw(amount)
        receiver_account.deposit(amount)
        
        # Override auto-recorded default transaction names for clear context
        sender_account._transactions[-1]["Type"] = "Transfer Sent"
        receiver_account._transactions[-1]["Type"] = "Transfer Received"

        self.save_accounts()
        return True

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