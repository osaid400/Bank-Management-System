# Bank Management System
# Author: Muhammad Abdullah Farooq
# Language: Python
# Level: Beginner

import json
import os
import sys

print("============ Welcome to Bank Managment System =============")

class BankAccount:
    def __init__(self, holder_name, account_number, balance):
        self.holder_name = holder_name
        self.account_number = account_number
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

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
        return f"Account Holder: {self.holder_name}\nAccount Number: {self.account_number}\nBalance: {self.__balance}"

    def to_dict(self):
        return {
            "Holder_name": self.holder_name,
            "Account_number": self.account_number,
            "Balance": self.__balance
        }

    @classmethod
    def from_dict(cls, account_data):
        return cls(
            holder_name=account_data["Holder_name"],
            account_number=account_data["Account_number"],
            balance=account_data["Balance"]
        )

# MAINTENANCE: ================================================================

class Bank_Manager:
    def __init__(self, filename="accounts.json"):
        self.filename = filename
        self.accounts = []
        self.load_accounts()

        if not self.accounts:
            self.accounts = [
        BankAccount("Ali", 3011, 15000),
        BankAccount("Abdullah", 3012, 23500),
        BankAccount("Ahmed", 3013, 23500),
        BankAccount("Zohaib", 3014, 55500),
        BankAccount("Fabiha", 3015, 13500),
        BankAccount("Rida", 3016, 52000),
        BankAccount("Asghar", 3017, 32500),
        BankAccount("Zayan", 3018, 76500),
        BankAccount("Askhay Kumar", 3019, 40000),
        BankAccount("Obaid", 3020, 45000),
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
            json.dump(self.accounts, file, indent=3)

    def create_account(self):
        name = input("Enter the Name: ").strip()
        if name == "":
            print("Name cannot be empty!")
            return

        try:
            account_number = int(input("Enter the new account ID: "))
        except ValueError:
            print("Invalid account ID! Please enter a number.")
            return

        if account_number <= 0:
            print("Enter a valid account ID!")
            return

        if Bank_Manager.find_account(account_number) is not None:
            print("Account ID already exists!")
            return

        try:
            balance = int(input("Enter the initial balance: "))
        except ValueError:
            print("Invalid Balance!")
            return

        if balance < 0:
            print("Initial Balance cannot be Negative!")
            return

        Bank_Manager.accounts.append(BankAccount(name, account_number, balance))
        Bank_Manager.save_accounts()
        print("New Account Added Successfully!")

    def view_account(self):
        if not Bank_Manager.accounts:
            print("No accounts available.")
            return

        for account in Bank_Manager.accounts:
            print("---------------------------------------------------")
            print("Name:", account.holder_name)
            print("Balance:", account.balance)
            print("Account Number:", account.account_number)
            print("---------------------------------------------------")

    def deposit_money(self):
        try:
            search = int(input("Enter the Account number: "))
        except ValueError:
            print("Invalid Account Number!")
            return

        account = Bank_Manager.find_account(search)
        if account is None:
            print("Account Not Found")
            return

        print("Account Found Successfully!")
        try:
            amount = int(input("Enter Amount: "))
        except ValueError:
            print("Invalid Amount!")
            return

        try:
            account.deposit(amount)
        except ValueError as error:
            print(error)
            return

        Bank_Manager.save_accounts()
        print("Money Deposit Successfully!")

    def withdraw_money(self):
        try:
            search = int(input("Enter the Account number: "))
        except ValueError:
            print("Invalid Account Number!")
            return

        account = Bank_Manager.find_account(search)
        if account is None:
            print("Account Not Found")
            return

        print("Account Found Successfully!")
        try:
            amount = int(input("Enter Amount: "))
        except ValueError:
            print("Invalid Amount!")
            return

        try:
            account.withdraw(amount)
        except ValueError as error:
            print(error)
            return

        Bank_Manager.save_accounts()
        print("Money Withdraw Successfully!")

    def check_balance(self):
        try:
            search = int(input("Enter the Account number: "))
        except ValueError:
            print("Invalid Account Number!")
            return

        account = Bank_Manager.find_account(search)
        if account is None:
            print("Account Not Found")
            return

        print("-" * 60)
        print("Account Found Successfully!")
        print("The Balance is:", account.balance)
        print("-" * 60)

    def delete_account(self):
        try:
            search = int(input("Enter the account number: "))
        except ValueError:
            print("Invalid Account Number!")
            return

        account = Bank_Manager.find_account(search)
        if account is None:
            print("Account Not Found")
            return

        choice = input("Are you sure? (y/n): ").lower()
        if choice != "y":
            print("Delete Cancelled!")
            return

        Bank_Manager.accounts.remove(account)
        Bank_Manager.save_accounts()
        print("Account Deleted Successfully!")

# Menu
def main():
    print("============ Welcome to Contact Book System =============")
    Bank = Bank_Manager()

    while True:
        print()
        print("=============== Select the Option ===============")
        print("1. Create Account")
        print("2. View Accounts")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Check Balance")
        print("6. Delete Account")
        print("0. Exit")

        try:
            choice = int(input("Enter the number (0-6): "))
        except ValueError:
            print("Invalid Number!")
            continue

        if choice == 1:
            Bank.create_account()
        elif choice == 2:
            Bank.view_account()
        elif choice == 3:
            Bank.deposit_money()
        elif choice == 4:
            Bank.withdraw_money()
        elif choice == 5:
            Bank.check_balance()
        elif choice == 6:
            Bank.delete_account()
        elif choice == 0:
            print("============ Exiting the Application =============")
            print("Thank You for using our application :)")
            print("Good Bye!")
            print("===================================================")
            sys.exit()
        else:
            print("Invalid Choice!")

main()