# src/ui.py
import sys

def print_mini_statement(account, limit=5):
    transactions = list(reversed(account._transactions))[:limit]
    print("\n" + "=" * 60)
    print(f"Mini Statement for {account.name} ({account.account_number})")
    print("=" * 60)
    print(f"Current Balance: Rs. {account.balance:,.2f}")
    if not transactions:
        print("No transactions recorded yet.")
    else:
        for tx in transactions:
            tx_type = tx.get("Type", "Unknown")
            amount = tx.get("Amount", 0.0)
            date = tx.get("Date", "----/--/--")
            time = tx.get("Time", "--:--:--")
            print(f"{date} {time} | {tx_type:<15} | Rs. {amount:,.2f}")
    print("=" * 60)

def print_cash_statement(account, days=30):
    statement = account.statement(days=days)
    print("\n" + "=" * 60)
    print(f"         {days}-Day Cash Statement for {account.name} ({account.account_number})")
    print("=" * 60)
    print(f"Current Balance: Rs. {account.balance:,.2f}")
    print(f"Last {days} days transactions:")
    print("-" * 60)

    if not statement:
        print(f"No deposits or withdrawals found in the last {days} days.")
        print("=" * 60)
        return

    header = f"{'Date':<12} {'Time':<10} {'Type':<15} {'Amount':>14}"
    print(header)
    print("-" * 60)

    for tx in statement:
        tx_type = tx.get("Type", "Unknown")
        amount = tx.get("Amount", 0.0)
        date = tx.get("Date", "----/--/--")
        time = tx.get("Time", "--:--:--")
        print(f"{date:<12} {time:<10} {tx_type:<15} Rs. {amount:>10,.2f}")

    print("=" * 60)

def run_bank_menu(manager, account):
    while True:
        print("\n" + "=" * 60)
        print(f"Welcome Back, {account.name}".center(60))
        print("=" * 60)
        print("1. Check Balance\n2. Deposit Money\n3. Withdraw Money")
        print("4. Change Pin\n5. Cash Statement (30 Days)\n6. Transfer Money")
        print("7. Mini Statement\n8. Logout\n0. Back to Main Menu")
        print("-" * 60)

        choice = input("Enter choice: ").strip()

        if choice == "1":
            print(f"\nCurrent Balance: Rs. {account.balance:,.2f}")

        elif choice == "2":
            try:
                amount = float(input("Enter Amount to Deposit: "))
                account.deposit(amount)
                manager.save_accounts()
                r_path = manager.generate_receipt(account, "Deposit", amount, "Cash Deposit")
                print(f"Deposit Successful! Balance: Rs. {account.balance:,.2f}")
                print(f"Receipt saved to: {r_path}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            try:
                amount = float(input("Enter Amount to Withdraw: "))
                account.withdraw(amount)
                manager.save_accounts()
                r_path = manager.generate_receipt(account, "Withdrawal", amount, "Cash Withdrawal")
                print(f"Withdrawal Successful! Balance: Rs. {account.balance:,.2f}")
                print(f"Receipt saved to: {r_path}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            old_pin = input("Enter current PIN: ").strip()
            new_pin = input("Enter new PIN: ").strip()
            try:
                account.change_pin(old_pin, new_pin)
                manager.save_accounts()
                print("PIN changed successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            print_cash_statement(account, days=30)

        elif choice == "6":
            try:
                rec_num = int(input("Enter recipient account number: "))
                rec_acc = manager.find_account(rec_num)
                if not rec_acc:
                    print("Recipient account not found.")
                    continue
                amount = float(input("Enter transfer amount: "))
                manager.transfer_money(account, rec_acc, amount)
                manager.generate_receipt(account, "Transfer Sent", amount, f"To {rec_acc.name}", "sent")
                manager.generate_receipt(rec_acc, "Transfer Received", amount, f"From {account.name}", "received")
                print("Money Transferred Successfully!")
            except ValueError as e:
                print(f"Transfer Failed: {e}")

        elif choice == "7":
            print_mini_statement(account, limit=5)

        elif choice in ["8", "0"]:
            print("Logged out successfully.")
            break
        else:
            print("Invalid Choice!")

def start_app(manager):
    while True:
        print("\n" + "=" * 60)
        print("WELCOME TO BANK MANAGEMENT SYSTEM".center(60))
        print("=" * 60)
        print("1. Login\n0. Exit")
        print("-" * 60)

        choice = input("Enter choice: ").strip()
        if choice == "1":
            try:
                acc_num = int(input("Enter Account Number: "))
                pin = input("Enter 4-digit PIN: ").strip()
                acc = manager.find_account(acc_num)
                if acc and acc.verify_pin(pin):
                    print("Login Successful!")
                    run_bank_menu(manager, acc)
                else:
                    print("Invalid Account Number or PIN.")
            except ValueError:
                print("Invalid input format.")
        elif choice == "0":
            print("Thank you for using our Bank Application. Good Bye!")
            sys.exit()
        else:
            print("Invalid Choice!")