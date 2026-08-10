import hashlib
from datetime import datetime, timedelta

class BankAccount:

    def __init__(self, name, account_number, balance, pin, account_type="Savings", loan_balance=0.0, pending_loan=0.0, transactions=None, checkbook_status="None", is_active=True, pin_is_hashed=False):
        self.__balance = float(balance)
        self.name = name
        self.account_number = int(account_number)
        self.account_type = account_type
        self.loan_balance = float(loan_balance)
        self.pending_loan = float(pending_loan)
        self.checkbook_status = checkbook_status
        self.is_active = is_active
        self._transactions = transactions or []

        pin_str = str(pin).strip()
        if pin_is_hashed:
            self.__pin_hash = pin_str
        else:
            self.__pin_hash = self._hash_pin(pin_str)

    @staticmethod
    def _hash_pin(pin_str):
        clean_pin = str(pin_str).zfill(4)
        return hashlib.sha256(clean_pin.encode("utf-8")).hexdigest()

    @property
    def balance(self):
        return self.__balance

    def verify_pin(self, input_pin):
        return self._hash_pin(input_pin) == self.__pin_hash

    def check_active_status(self):
        if not self.is_active:
            raise ValueError("Account is FROZEN! Please contact bank administration.")

    def get_daily_withdrawn_amount(self):
        today = datetime.now().strftime("%Y-%m-%d")
        total = 0.0
        for tx in self._transactions:
            if tx.get("Date") == today and tx.get("Type") in ["Withdrawal", "Transfer Sent"]:
                total += tx.get("Amount", 0.0)
        return total

    def calculate_interest(self, rate=0.05):
        if self.account_type != "Savings":
            return 0
        interest = self.__balance * (rate / 12)
        self.__balance += interest
        self.record_transaction("Interest Credited", interest)
        return interest

    def record_transaction(self, transaction_type, amount):
        now = datetime.now()
        self._transactions.append({
            "Type": transaction_type,
            "Amount": float(amount),
            "Date": now.strftime("%Y-%m-%d"),
            "Time": now.strftime("%H:%M:%S")
        })

    def deposit(self, amount):
        self.check_active_status()
        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero!")
        if amount > 100000:
            raise ValueError("Single transaction limit exceeded! (Max Rs. 100,000)")
        
        self.__balance += amount
        self.record_transaction("Deposit", amount)

    def withdraw(self, amount):
        self.check_active_status()
        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero!")
        if amount > 100000:
            raise ValueError("Single transaction limit exceeded! (Max Rs. 100,000)")

        daily_spent = self.get_daily_withdrawn_amount()
        if daily_spent + amount > 200000:
            raise ValueError(f"Daily withdrawal limit of Rs. 200,000 exceeded! Already used today: Rs. {daily_spent:,.2f}")

        min_allowed_balance = 2000.0 if self.account_type == "Savings" else -50000.0
        if (self.__balance - amount) < min_allowed_balance:
            if self.account_type == "Savings":
                raise ValueError("Savings Account requires a minimum balance of Rs. 2,000!")
            else:
                raise ValueError("Current Account overdraft limit of Rs. 50,000 exceeded!")

        self.__balance -= amount
        self.record_transaction("Withdrawal", amount)

    def apply_loan(self, amount):
        self.check_active_status()
        if self.loan_balance > 0:
            raise ValueError("You already have an active loan.")
        if self.pending_loan > 0:
            raise ValueError("You already have a loan request pending approval.")
        
        max_loan = max(self.__balance, 1000) * 5
        if amount <= 0 or amount > max_loan:
            raise ValueError(f"Loan amount must be between 1 and {max_loan:.2f}")
        
        self.pending_loan = float(amount)
        self.record_transaction("Loan Requested", amount)

    def reject_loan(self):
        if self.pending_loan <= 0:
            raise ValueError("No pending loan request to reject.")
        rejected_amt = self.pending_loan
        self.pending_loan = 0.0
        self.record_transaction("Loan Rejected", rejected_amt)

    def return_loan(self, amount):
        self.check_active_status()
        if amount <= 0 or amount > self.loan_balance:
            raise ValueError("Invalid repayment amount.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance to repay loan.")
        self.__balance -= amount
        self.loan_balance -= amount
        self.record_transaction("Loan Repayment", amount)

    def request_checkbook(self):
        self.check_active_status()
        if self.checkbook_status == "Pending":
            raise ValueError("Checkbook request is already pending approval.")
        self.checkbook_status = "Pending"
        self.record_transaction("Checkbook Requested", 0)

    def reject_checkbook(self):
        if self.checkbook_status != "Pending":
            raise ValueError("No pending checkbook request to reject.")
        self.checkbook_status = "Rejected"
        self.record_transaction("Checkbook Rejected", 0)

    def change_pin(self, old_pin, new_pin):
        self.check_active_status()
        if not self.verify_pin(old_pin):
            raise ValueError("Incorrect current PIN!")
        new_pin_str = str(new_pin).strip().zfill(4)
        if not new_pin_str.isdigit() or len(new_pin_str) != 4:
            raise ValueError("PIN must be exactly 4 digits!")
        self.__pin_hash = self._hash_pin(new_pin_str)
        self.record_transaction("PIN Changed", 0)

    def to_dict(self):
        return {
            "Holder_name": self.name,
            "Account_number": self.account_number,
            "Balance": self.__balance,
            "PIN_HASH": self.__pin_hash,
            "Account_Type": self.account_type,
            "Loan_Balance": self.loan_balance,
            "Pending_Loan": self.pending_loan,
            "Checkbook_Status": self.checkbook_status,
            "Is_Active": self.is_active,
            "Transactions": self._transactions
        }

    @classmethod
    def from_dict(cls, account_data):
        pin_hash = account_data.get("PIN_HASH")
        cb_status = account_data.get("Checkbook_Status")
        if cb_status is None:
            cb_status = "Pending" if account_data.get("Checkbook_Requested") else "None"

        is_active = account_data.get("Is_Active", True)

        if pin_hash:
            return cls(
                name=account_data.get("Holder_name") or account_data.get("Name") or account_data.get("name"),
                account_number=account_data.get("Account_number") or account_data.get("Account Number") or account_data.get("account_number"),
                balance=account_data.get("Balance") if account_data.get("Balance") is not None else account_data.get("balance", 0.0),
                pin=pin_hash,
                account_type=account_data.get("Account_Type") or account_data.get("Account_type") or account_data.get("account_type", "Savings"),
                loan_balance=account_data.get("Loan_Balance") if account_data.get("Loan_Balance") is not None else account_data.get("Loan_balance", 0.0),
                pending_loan=account_data.get("Pending_Loan", 0.0),
                transactions=account_data.get("Transactions") or account_data.get("transactions", []),
                checkbook_status=cb_status,
                is_active=is_active,
                pin_is_hashed=True
            )
        
        raw_pin = str(account_data.get("PIN") or account_data.get("pin") or "1234")
        return cls(
            name=account_data.get("Holder_name") or account_data.get("Name") or account_data.get("name"),
            account_number=account_data.get("Account_number") or account_data.get("Account Number") or account_data.get("account_number"),
            balance=account_data.get("Balance") if account_data.get("Balance") is not None else account_data.get("balance", 0.0),
            pin=raw_pin,
            account_type=account_data.get("Account_Type") or account_data.get("Account_type") or account_data.get("account_type", "Savings"),
            loan_balance=account_data.get("Loan_Balance") if account_data.get("Loan_Balance") is not None else account_data.get("Loan_balance", 0.0),
            pending_loan=account_data.get("Pending_Loan", 0.0),
            transactions=account_data.get("Transactions") or account_data.get("transactions", []),
            checkbook_status=cb_status,
            is_active=is_active,
            pin_is_hashed=False
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