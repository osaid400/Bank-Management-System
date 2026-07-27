# Bank Management System
# Author: Muhammad Abdullah Farooq
# Language: Python

import json
import os
import sys

class BankAccount:
    def __init__(self, holder_name, account_number, balance, pin):
        self.holder_name = holder_name
        self.account_number = account_number
        self.__balance = float(balance)
        self.__pin = str(pin)

    @property
    def balance(self):
        return self.__balance

    def verify_pin(self, input_pin):
        return str(input_pin) == self.__pin

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero!")
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero!")
        if amount > self.__balance:
            raise ValueError("Insufficient Balance!")
        self.__balance -= amount

    def __str__(self):
        return (
            f"Account Holder: {self.holder_name}\n"
            f"Account Number: {self.account_number}\n"
            f"Balance       : {self.__balance:.2f}"
        )

    def to_dict(self):
        return {
            "Holder_name": self.holder_name,
            "Account_number": self.account_number,
            "Balance": self.__balance,
            "PIN": self.__pin
        }

    @classmethod
    def from_dict(cls, account_data):
        return cls(
            holder_name=account_data["Holder_name"],
            account_number=account_data["Account_number"],
            balance=account_data["Balance"],
            pin=str(account_data.get("PIN", "1234"))
        )


class BankManager:
    def __init__(self, filename="accounts.json"):
        self.filename = filename
        self.accounts = []
        self.load_accounts()

        if not self.accounts:
            self.accounts = [
                BankAccount("Ali", 3011, 15000, "1234"),
                BankAccount("Abdullah", 3012, 23500, "1234"),
                BankAccount("Ahmed", 3013, 23500, "1234"),
                BankAccount("Zohaib", 3014, 55500, "1234"),
                BankAccount("Fabiha", 3015, 13500, "1234"),
                BankAccount("Rida", 3016, 52000, "1234"),
                BankAccount("Asghar", 3017, 32500, "1234"),
                BankAccount("Zayan", 3018, 76500, "1234"),
                BankAccount("Akshay Kumar", 3019, 40000, "1234"),
                BankAccount("Obaid", 3020, 45000, "1234"),
            ]
            self.save_accounts()

    def load_accounts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.accounts = [BankAccount.from_dict(item) for item in data]
            except (json.JSONDecodeError, ValueError, OSError):
                self.accounts = []
        else:
            self.accounts = []

    def save_accounts(self):
        with open(self.filename, "w") as file:
            data = [account.to_dict() for account in self.accounts]
            json.dump(data, file, indent=4)

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def authenticate(self, account):
        pin_input = input("Enter 4-digit PIN: ").strip()

        if not pin_input.isdigit():
            print("Invalid PIN format! PIN must contain numbers only.")
            return False

        if not account.verify_pin(pin_input):
            print("Incorrect PIN! Access Denied.")
            return False

        return True

    def create_account(self):
        name = input("Enter the Name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return

        try:
            account_number = int(input("Enter the new account ID: "))
        except ValueError:
            print("Invalid account ID! Please enter a valid number.")
            return

        if account_number <= 0:
            print("Enter a valid account ID!")
            return

        if self.find_account(account_number) is not None:
            print("Account ID already exists!")
            return

        try:
            balance = float(input("Enter the initial balance: "))
        except ValueError:
            print("Invalid Balance!")
            return

        if balance < 0:
            print("Initial Balance cannot be Negative!")
            return

        pin = input("Set a 4-digit PIN: ").strip()

        if len(pin) != 4 or not pin.isdigit():
            print("Invalid PIN! PIN must contain exactly 4 numeric digits (e.g., 1234).")
            return

        self.accounts.append(BankAccount(name, account_number, balance, pin))
        self.save_accounts()
        print("New Account Created Successfully!")

    def view_accounts(self):
        if not self.accounts:
            print("No accounts available.")
            return

        print("\n--- ALL ACCOUNTS DIRECTORY ---")
        for account in self.accounts:
            print("-" * 51)
            print("Name          :", account.holder_name)
            print("Account Number:", account.account_number)
            print("Balance       : [Hidden - Requires PIN Authentication]")
            print("-" * 51)

    def search_account(self):
        if not self.accounts:
            print("No accounts available in system.")
            return

        query = input("Enter Account Number or Holder Name to Search: ").strip()
        if not query:
            print("Search input cannot be empty!")
            return

        matches = []
        for account in self.accounts:
            if query == str(account.account_number) or query.lower() in account.holder_name.lower():
                matches.append(account)

        if not matches:
            print("No matching account found!")
            return

        print(f"\n--- SEARCH RESULTS ({len(matches)} Found) ---")
        for account in matches:
            print("-" * 51)
            print("Name          :", account.holder_name)
            print("Account Number:", account.account_number)
            print("Balance       : [Hidden - Requires PIN Authentication]")
            print("-" * 51)

    def deposit_money(self):
        try:
            search = int(input("Enter the Account number: "))
        except ValueError:
            print("Invalid Account Number!")
            return

        account = self.find_account(search)
        if account is None:
            print("Account Not Found")
            return

        if not self.authenticate(account):
            return

        try:
            amount = float(input("Enter Amount: "))
        except ValueError:
            print("Invalid Amount!")
            return

        try:
            account.deposit(amount)
        except ValueError as error:
            print(error)
            return

        self.save_accounts()
        print("Money Deposited Successfully!")
        print("\nUpdated Account Details:")
        print(account)

    def withdraw_money(self):
        try:
            search = int(input("Enter the Account number: "))
        except ValueError:
            print("Invalid Account Number!")
            return

        account = self.find_account(search)
        if account is None:
            print("Account Not Found")
            return

        if not self.authenticate(account):
            return

        try:
            amount = float(input("Enter Amount: "))
        except ValueError:
            print("Invalid Amount!")
            return

        try:
            account.withdraw(amount)
        except ValueError as error:
            print(error)
            return

        self.save_accounts()
        print("Money Withdrawn Successfully!")
        print("\nUpdated Account Details:")
        print(account)

    def check_balance(self):
        try:
            search = int(input("Enter the Account number: "))
        except ValueError:
            print("Invalid Account Number!")
            return

        account = self.find_account(search)
        if account is None:
            print("Account Not Found")
            return

        if not self.authenticate(account):
            return

        print("-" * 60)
        print("Account Found Successfully!\n")
        print(account)
        print("-" * 60)

    def delete_account(self):
        try:
            search = int(input("Enter the account number: "))
        except ValueError:
            print("Invalid Account Number!")
            return

        account = self.find_account(search)
        if account is None:
            print("Account Not Found")
            return

        if not self.authenticate(account):
            return

        choice = input("Are you sure you want to delete this account? (y/n): ").strip().lower()
        if choice != "y":
            print("Delete Cancelled!")
            return

        self.accounts.remove(account)
        self.save_accounts()
        print("Account Deleted Successfully!")


def main():
    print("============ Welcome to Bank Management System =============")
    bank = BankManager()

    while True:
        print("\n=============== Select Option ===============")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. Search Account")
        print("4. Deposit Money")
        print("5. Withdraw Money")
        print("6. Check Balance")
        print("7. Delete Account")
        print("0. Exit")

        try:
            choice = int(input("Enter option (0-7): "))
        except ValueError:
            print("Invalid Number!")
            continue

        if choice == 1:
            bank.create_account()
        elif choice == 2:
            bank.view_accounts()
        elif choice == 3:
            bank.search_account()
        elif choice == 4:
            bank.deposit_money()
        elif choice == 5:
            bank.withdraw_money()
        elif choice == 6:
            bank.check_balance()
        elif choice == 7:
            bank.delete_account()
        elif choice == 0:
            print("============ Exiting Application =============")
            print("Thank you for using our application :)")
            print("Good Bye!")
            print("===================================================")
            sys.exit()
        else:
            print("Invalid Choice!")


main()