# src/models.py

from datetime import datetime, timedelta

class BankAccount:

    def __init__(self, name, account_number, balance, pin, transactions=None):
        self.__balance = float(balance)
        self.__pin = str(pin).zfill(4)
        self.name = name
        self.account_number = account_number
        self._transactions = transactions or []

    @property
    def balance(self):
        return self.__balance

    def verify_pin(self, input_pin):
        return str(input_pin).zfill(4) == self.__pin

    def record_transaction(self, transaction_type, amount):
        now = datetime.now()
        self._transactions.append({
            "Type": transaction_type,
            "Amount": float(amount),
            "Date": now.strftime("%Y-%m-%d"),
            "Time": now.strftime("%H:%M:%S")
        })

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero!")
        self.__balance += amount
        self.record_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero!")
        if amount > self.__balance:
            raise ValueError("Insufficient Balance!")
        self.__balance -= amount
        self.record_transaction("Withdrawal", amount)

    def apply_loan(self):
        ...

    def return_loan(self):
        ...

    def apply_checkbook(self):
        ...

    def close_account(self):
        ...

    def change_pin(self, old_pin, new_pin):
        if not self.verify_pin(old_pin):
            raise ValueError("Incorrect current PIN!")
        new_pin_str = str(new_pin).zfill(4)
        if not new_pin_str.isdigit() or len(new_pin_str) != 4:
            raise ValueError("PIN must be exactly 4 digits!")
        self.__pin = new_pin_str
        self.record_transaction("PIN Changed", 0)

    def to_dict(self):
        return {
            "Holder_name": self.name,
            "Account_number": self.account_number,
            "Balance": self.__balance,
            "PIN": self.__pin,
            "Transactions": self._transactions
        }

    @classmethod
    def from_dict(cls, account_data):
        return cls(
            name=account_data.get("Holder_name") or account_data.get("Name"),
            account_number=account_data.get("Account_number") or account_data.get("Account Number"),
            balance=account_data.get("Balance", 0),
            pin=str(account_data.get("PIN", "1234")),
            transactions=account_data.get("Transactions", [])
        )

    def statement(self, days=30):
        cutoff = datetime.now() - timedelta(days=days)
        recent_transactions = []
        for tx in self._transactions:
            try:
                tx_datetime = datetime.strptime(f"{tx['Date']} {tx['Time']}", "%Y-%m-%d %H:%M:%S")
                if tx_datetime >= cutoff:
                    recent_transactions.append(tx)
            except (KeyError, ValueError):
                continue
        return recent_transactions