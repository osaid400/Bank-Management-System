# Bank Management System

A console-based **Bank Management System** built with Python using **Object-Oriented Programming (OOP)**. This project demonstrates clean class design, private attributes, PIN authentication, JSON-based data persistence, input validation, exception handling, and CRUD-style account management.

## Features

* Create a new bank account
* View all accounts
* Search accounts by account number or holder name
* Deposit money
* Withdraw money
* Check account balance
* Delete an account
* PIN authentication for sensitive actions
* Prevent duplicate account numbers
* Validate user input
* Persistent storage using JSON
* Automatically load saved accounts on startup
* Clean OOP design using `BankAccount` and `BankManager` classes

## Technologies Used

* Python 3
* JSON

## Concepts Covered

### Python Fundamentals

* Functions
* Conditional Statements
* Loops
* Exception Handling
* User Input
* Data Validation
* File Handling with JSON (`json.load()`, `json.dump()`)
* `os.path.exists()`
* String Methods (`strip()`, `lower()`, `isdigit()`)

### Object-Oriented Programming (OOP)

* Classes & Objects
* Constructors (`__init__`)
* Encapsulation
* Private Attributes
* Properties (`@property`)
* Class Methods (`@classmethod`)
* Object Serialization (`to_dict()`, `from_dict()`)
* `__str__()` Magic Method
* Composition

## Project Structure

```text
Bank-Management-System/
│
├── Bank Management System.py
├── .gitignore
└── README.md
```

> **Note:** `accounts.json` is created automatically when the program runs. It stores account data locally and is excluded from the repository through `.gitignore` because it contains runtime data rather than source code.

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/osaid400/Bank-Management-System.git
```

2. Navigate to the project folder:

```bash
cd Bank-Management-System
```

3. Run the program:

```bash
python "Bank Management System.py"
```

## Example Output

### Main Menu

```text
============ Welcome to Bank Management System =============

=============== Select Option ===============
1. Create Account
2. View Accounts
3. Search Account
4. Deposit Money
5. Withdraw Money
6. Check Balance
7. Delete Account
0. Exit
===============================================
```

### Searching an Account

```text
Enter Account Number or Holder Name to Search: Ali

--- SEARCH RESULTS (1 Found) ---
---------------------------------------------------
Name            : Ali
Account Number  : 3011
Balance         : [Hidden - Requires PIN Authentication]
---------------------------------------------------
```

### Checking Balance

```text
Enter the Account number: 3011
Enter 4-digit PIN: 1234
------------------------------------------------------------
Account Found Successfully!

Account Holder  : Ali
Account Number  : 3011
Balance         : 15000.00
------------------------------------------------------------
```

## How Data Persistence Works

* When the application starts, it checks whether `accounts.json` exists.
* If the file exists, all account records are loaded and converted into `BankAccount` objects.
* If the file does not exist, the program starts with a default set of sample accounts and saves them to `accounts.json`.
* Whenever an account is created, updated through deposit or withdrawal, or deleted, the full account list is saved back to `accounts.json`.
* This ensures that account data remains available even after closing and reopening the program.

## Future Improvements

* Add transaction history
* Add account types (Savings / Current)
* Transfer money between accounts
* Improve PIN security with hashing
* Store data using SQLite instead of JSON
* Build a GUI version using Tkinter
* Add account statement / mini statement

## Learning Outcomes

This project helped me practice:

* Designing applications using Object-Oriented Programming
* Creating reusable classes and objects
* Applying encapsulation with private attributes
* Using properties and class methods
* Managing persistent data with JSON
* Building a menu-driven console application
* Handling exceptions and validating user input
* Writing clean, maintainable, and modular Python code

## Author

**Muhammad Abdullah Farooq**

GitHub: https://github.com/osaid400
