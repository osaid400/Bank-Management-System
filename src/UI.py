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
            print(f"{date} {time} | {tx_type:<18} | Rs. {amount:,.2f}")
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

    header = f"{'Date':<12} {'Time':<10} {'Type':<18} {'Amount':>14}"
    print(header)
    print("-" * 60)

    for tx in statement:
        tx_type = tx.get("Type", "Unknown")
        amount = tx.get("Amount", 0.0)
        date = tx.get("Date", "----/--/--")
        time = tx.get("Time", "--:--:--")
        print(f"{date:<12} {time:<10} {tx_type:<18} Rs. {amount:>10,.2f}")

    print("=" * 60)

def print_full_bank_report(manager):
    summary = manager.generate_bank_report()
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE BANK FINANCIAL & ACTIVITY REPORT".center(80))
    print("=" * 80)
    
    print("\n--- GLOBAL FINANCIAL SUMMARY ---")
    for k, v in summary.items():
        if isinstance(v, (float, int)) and "Total" in k and "Customers" not in k and "Transactions" not in k and "Accounts" not in k:
            print(f"{k:<32}: Rs. {v:,.2f}")
        else:
            print(f"{k:<32}: {v}")

    print("\n--- ALL CUSTOMER ACCOUNTS OVERVIEW ---")
    print(f"{'Acc No':<8} {'Name':<15} {'Type':<10} {'Status':<10} {'Balance':<14} {'Active Loan':<12}")
    print("-" * 80)
    for acc in manager.accounts:
        status_str = "ACTIVE" if acc.is_active else "FROZEN"
        print(f"{acc.account_number:<8} {acc.name:<15} {acc.account_type:<10} {status_str:<10} Rs.{acc.balance:<11,.0f} Rs.{acc.loan_balance:<10,.0f}")
    print("=" * 80)

def run_bank_menu(manager, account):
    while True:
        print("\n" + "=" * 60)
        status_label = "" if account.is_active else " [ACCOUNT FROZEN]"
        print(f"Welcome Back, {account.name}{status_label}".center(60))
        print("=" * 60)
        print("1. Check Balance\n2. Deposit Money\n3. Withdraw Money")
        print("4. Change Pin\n5. Cash Statement (30 Days)\n6. Transfer Money")
        print("7. Mini Statement\n8. Request Checkbook\n9. Apply Loan\n10. Return Loan\n11. Logout\n0. Back to Main Menu")
        print("-" * 60)

        choice = input("Enter choice: ").strip()

        if choice == "1":
            print(f"\nCurrent Balance: Rs. {account.balance:,.2f}")
            print(f"Account Type   : {account.account_type}")
            print(f"Account Status : {'Active' if account.is_active else 'FROZEN'}")
            if account.pending_loan > 0:
                print(f"Pending Loan Request: Rs. {account.pending_loan:,.2f}")
            print(f"Checkbook Status: {account.checkbook_status}")

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

        elif choice == "8":
            try:
                account.request_checkbook()
                manager.save_accounts()
                print("Checkbook request submitted! Awaiting admin approval.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "9":
            try:
                amount = float(input("Enter loan amount to apply for: "))
                account.apply_loan(amount)
                manager.save_accounts()
                print(f"Loan application of Rs. {amount:,.2f} submitted! Awaiting admin approval.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "10":
            try:
                amount = float(input("Enter loan repayment amount: "))
                account.return_loan(amount)
                manager.save_accounts()
                print(f"Loan repayment of Rs. {amount:,.2f} successful!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice in ["11", "0"]:
            print("Logged out successfully.")
            break

        else:
            print("Invalid Choice!")

def run_admin_menu(manager):
    while True:
        print("\n" + "=" * 60)
        print("ADMIN PORTAL".center(60))
        print("=" * 60)
        print("1. Open New Account")
        print("2. Close Account")
        print("3. Freeze / Unfreeze Account")
        print("4. Manage Loan Requests (Approve/Reject)")
        print("5. Manage Checkbook Requests (Approve/Reject)")
        print("6. View Complete Bank Report & Activities")
        print("7. Apply Monthly Interest to All Accounts")
        print("0. Logout")
        print("-" * 60)

        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                name = input("Enter customer name: ").strip()
                initial_deposit = float(input("Enter initial deposit: "))
                pin = input("Enter 4-digit PIN: ").strip()
                account_type = input("Enter account type (Savings/Current): ").strip()

                new_account = manager.open_account(name, initial_deposit, pin, account_type)
                print(f"Account opened successfully for {new_account.name} with Auto-Assigned Account Number: {new_account.account_number}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            try:
                account_number = int(input("Enter account number to close: "))
                account = manager.find_account(account_number)
                if account:
                    manager.close_account(account)
                    print(f"Account {account_number} closed successfully.")
                else:
                    print("Account not found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            try:
                account_number = int(input("Enter account number: "))
                account = manager.find_account(account_number)
                if account:
                    new_status = manager.toggle_account_status(account)
                    status_text = "ACTIVATED" if new_status else "FROZEN"
                    print(f"Account {account.account_number} for {account.name} is now {status_text}.")
                else:
                    print("Account not found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            pending_loans = [acc for acc in manager.accounts if acc.pending_loan > 0]
            if not pending_loans:
                print("No pending loan requests found.")
                continue

            print("\n--- PENDING LOAN REQUESTS ---")
            for acc in pending_loans:
                print(f"Account: {acc.account_number} | Name: {acc.name} | Requested: Rs. {acc.pending_loan:,.2f}")

            try:
                account_number = int(input("\nEnter account number to process: "))
                account = manager.find_account(account_number)
                if account and account.pending_loan > 0:
                    action = input("Type 'A' to Approve or 'R' to Reject: ").strip().upper()
                    if action == "A":
                        manager.approve_loan(account)
                        print(f"Loan of Rs. {account.loan_balance:,.2f} approved for {account.name}.")
                    elif action == "R":
                        manager.reject_loan(account)
                        print(f"Loan request rejected for {account.name}.")
                    else:
                        print("Invalid action selection.")
                else:
                    print("Account not found or no pending loan.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            pending_cb = [acc for acc in manager.accounts if acc.checkbook_status == "Pending"]
            if not pending_cb:
                print("No pending checkbook requests found.")
                continue

            print("\n--- PENDING CHECKBOOK REQUESTS ---")
            for acc in pending_cb:
                print(f"Account: {acc.account_number} | Name: {acc.name}")

            try:
                account_number = int(input("\nEnter account number to process: "))
                account = manager.find_account(account_number)
                if account and account.checkbook_status == "Pending":
                    action = input("Type 'A' to Approve or 'R' to Reject: ").strip().upper()
                    if action == "A":
                        manager.approve_checkbook(account)
                        print(f"Checkbook request approved for {account.name}.")
                    elif action == "R":
                        manager.reject_checkbook(account)
                        print(f"Checkbook request rejected for {account.name}.")
                    else:
                        print("Invalid action selection.")
                else:
                    print("Account not found or no pending request.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "6":
            print_full_bank_report(manager)

        elif choice == "7":
            count = manager.apply_monthly_interest_to_all()
            print(f"Monthly interest credited successfully to {count} Savings accounts.")

        elif choice == "0":
            print("Exited Admin Portal.")
            break

        else:
            print("Invalid Choice!")

def start_app(manager):
    while True:
        print("\n" + "=" * 60)
        print("WELCOME TO BANK MANAGEMENT SYSTEM".center(60))
        print("=" * 60)
        print("1. Customer Login\n2. Admin Login\n0. Exit")
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

        elif choice == "2":
            username = input("Enter admin username: ").strip()
            password = input("Enter admin password: ").strip()
            if manager.admin_login(username, password):
                print("Admin Login Successful!")
                run_admin_menu(manager)
            else:
                print("Invalid Admin Credentials.")

        elif choice == "0":
            print("Thank you for using our Bank Application. Good Bye!")
            sys.exit()

        else:
            print("Invalid Choice!")