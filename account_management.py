# SecureBank - Module 1: Account Management (Milestone 1)
# - make one account (savings, checking, or time deposit)
# - view the account
# - manager can freeze then close it

from datetime import date, timedelta   # for the maturity date

import login_access_control
from ui_helpers import print_main_menu_account_management, print_divider
from login_access_control import is_branch_manager
# account variables
# these are global - module 2 uses them too

all_accounts = {}


current_role = ""          # set by accounts(), tells us who is logged in
has_account = False        # no account until we make one
acc_number = ""            # like BR01-00234
holder_name = ""           # customer's name
acc_type = ""              # Savings / Checking / TimeDeposit
balance = 0.0
status = ""                # Active -> Frozen -> Closed
interest_rate = 0.0        # in percent, 2.5 means 2.5%
min_balance = 0.0          # savings only, can't go below this
overdraft_limit = 0.0      # checking only, how far below zero we allow
term_days = 0              # time deposit only (30/60/90)
maturity_date = ""         # time deposit only, like "2026-11-16"

# account number = branch code + sequence
BRANCH_CODE = "BR01"
next_sequence = 234        # next number to give out, goes up by 1 every new account

# rules (capital letters so they're easier to change)
SAVINGS_RATE = 2.5
SAVINGS_MIN_BALANCE = 500.0
CHECKING_OVERDRAFT_LIMIT = 5000.0
TIME_DEPOSIT_MIN = 1000.0

# helper functions
# small functions that other functions (and module 2) reuse
def is_valid_amount(text):
    # checks if the input is a positive number like 500 or 500.75
    text = text.strip()
    if text == "":          # user just pressed enter
        return False
    # remove one dot then check if only digits are left
    # this blocks letters, negatives, and stuff like 1.2.3
    if text.replace(".", "", 1).isdigit() == False:
        return False
    # zero isn't a real deposit/withdrawal so reject it too
    if float(text) <= 0:
        return False
    return True

def ask_yes_no(prompt):
    # keeps asking until y or n, returns True if y
    while True:
        answer = input(prompt).strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("X Please type y or n.")

def make_account_number():
    # makes BR01-00234 then adds 1 to the counter for the next one
    global next_sequence
    number = f"{BRANCH_CODE}-{next_sequence:05d}"   # 05d = fill with zeros up to 5 digits
    next_sequence = next_sequence + 1
    return number

def get_time_deposit_rate(days):
    # longer term = higher rate
    if days == 30:
        return 3.25
    elif days == 60:
        return 4.00
    else:  # 90 days
        return 4.75

def find_account():
    if len(all_accounts) == 0:
        print("X No accounts exist yet. Create one first.")
        return ""

    entered = input("Enter account number: ").strip().upper()
    if entered not in all_accounts:
        print("X Account not found.")
        return ""
    return entered

# ---------- input functions ----------
# all of these loop until the input is valid so it never crashes
# on a wrong answer, it just asks again

def ask_account_type():
    while True:
        # lower() so "Savings", "savings", "SAVINGS" all work
        text = input("Enter account type (Savings/Checking/TimeDeposit): ").strip().lower()
        if text == "savings":
            return "Savings"
        elif text == "checking":
            return "Checking"
        elif text == "timedeposit" or text == "time deposit":
            return "TimeDeposit"
        else:
            print("X INVALID CHOICE. Try again")


def ask_term():
    while True:
        text = input("Enter deposit term (30/60/90 days): ").strip()
        if text == "30" or text == "60" or text == "90":
            return int(text)
        print("X Term must be 30, 60, or 90. Try again!")


def ask_initial_deposit(minimum):
    # minimum is different per account type
    while True:
        text = input("Enter initial deposit amount: ").strip()
        if is_valid_amount(text) == False:
            print("X INVALID AMOUNT. Enter a positive number.")
        elif float(text) < minimum:
            print(f"X Minimum opening deposit is PHP {minimum:,.2f}. Try again!")
        else:
            return float(text)


# 1. create account

def print_new_account(number):
        # shows the summary of a newly made account
        account = all_accounts[number]  # get this account's dictionary

        print("✔ Account created successfully!")
        print(f"Account Number: {number}")
        if account["acc_type"] == "TimeDeposit":
            print(f"Type: Time Deposit ({account['term_days']}-day term, matures {account['maturity_date']})")
            print(f"Interest Rate: {account['interest_rate']:.2f}% ({account['term_days']}-day tier)")
        elif account["acc_type"] == "Savings":
            print("Type: Savings")
            print(f"Interest Rate: {account['interest_rate']:.2f}%")
        else:
            print("Type: Checking")
            print(f"Overdraft Limit: PHP {account['overdraft_limit']:,.2f}")
        print(f"Balance: PHP {account['balance']:,.2f}")

    def create_account():

        name = input("Enter account holder name: ").strip()
        if name == "":
            print("X Name cannot be empty. Try again!")
            return

    chosen_type = ask_account_type()

# only save them at the end so nothing gets half saved if the user quits
    term = 0
    maturity = ""
    rate = 0.0
    min_bal = 0.0
    overdraft = 0.0
    opening_minimum = 0.01

    if chosen_type == "Savings":
        rate = SAVINGS_RATE
        min_bal = SAVINGS_MIN_BALANCE
        opening_minimum = SAVINGS_MIN_BALANCE     # has to open with at least 500
    elif chosen_type == "Checking":
        overdraft = CHECKING_OVERDRAFT_LIMIT
    else:  # time deposit
        term = ask_term()
        rate = get_time_deposit_rate(term)
        opening_minimum = TIME_DEPOSIT_MIN
        # today + the term = maturity date
        maturity = str(date.today() + timedelta(days=term))

    # initial deposit
    deposit = ask_initial_deposit(opening_minimum)

    # all valid. save the account into all_accounts
    number = make_account_number()
    all_accounts[number] = {
        "holder_name": name,
        "acc_type": chosen_type,
        "balance": deposit,
        "status": "Active",  # new accounts always start active
        "interest_rate": rate,
        "min_balance": min_bal,
        "overdraft_limit": overdraft,
        "term_days": term,
        "maturity_date": maturity,
    }

    print_new_account(number)



#  2. view account
# only reads the variables, doesn't change anything
def view_account():
    number = find_account()
    if number == "":
        return

    account = all_accounts[number]

    print_divider()
    print("ACCOUNT DETAILS")
    print_divider()
    # shown for all types
    print(f"Account Number : {acc_number}")
    print(f"Holder Name    : {holder_name}")
    if acc_type == "TimeDeposit":
        print("Account Type   : Time Deposit")
    else:
        print(f"Account Type   : {acc_type}")
    print(f"Status         : {status}")
    print(f"Balance        : PHP {balance:,.2f}")

    # extra lines per type
    if acc_type == "Savings":
        print(f"Interest Rate  : {interest_rate:.2f}%")
        print(f"Minimum Balance: PHP {min_balance:,.2f}")
    elif acc_type == "Checking":
        print(f"Overdraft Limit: PHP {overdraft_limit:,.2f}")
        print("Overdraft Fee  : PHP 50.00")
    else:
        print(f"Term           : {term_days} days")
        print(f"Interest Rate  : {interest_rate:.2f}%")
        print(f"Matures On     : {maturity_date}")
    print_divider()

# search accounts

def search_accounts():
    if len(all_accounts) == 0:
        print("X No accounts exist yet. Create one first.")
        return

    choice = input("Search by (1) Name or (2) Type: ").strip()
    if choice == "1":
        keyword = input("Enter name (or part of it): ").strip().lower()
        if keyword == "":
            print("X Search cannot be empty.")
            return
    elif choice == "2":
        keyword = ask_account_type()
    else:
        print("X Invalid choice. Enter 1 or 2.")
        return

    found = 0
    print_divider()
    # go through every account number in the dictionary
    for number in all_accounts:
        account = all_accounts[number]

        # check if this account matches what we searched
        is_match = False
        if choice == "1" and keyword in account["holder_name"].lower():
            is_match = True
        if choice == "2" and account["acc_type"] == keyword:
            is_match = True

        if is_match:
            result = f"{number} | {account['holder_name']} | PHP {account['balance']:,.2f} | {account['status']}"
            if account["acc_type"] == "TimeDeposit":
                result = result + f" | Matures {account['maturity_date']}"
            print(result)
            found = found + 1

    if found == 0:
        print("No accounts matched your search.")
    else:
        print(f"- Search Results ({found} found) -")
    print_divider()

# 3. freeze / close (manager only)
# Active -> Frozen -> Closed, one step each time
def freeze_or_close_account(staff):
    global status

    # check the role first, before anything else
    # this is the manager-only restriction
    if not is_branch_manager(staff):
        print("X ACCESS DENIED: Freezing/closing accounts requires Branch Manager privileges.")
        return

    if has_account == False:
        print("X No account exists yet.")
        return

    number = find_account()
    if number == "":
        return

    account = all_accounts[number]
    print(f"Current status: {account['status']}")


    if account["status"] == "Closed":
        print("X This account is already closed.")
    elif account["status"] == "Active":
        # active -> frozen
        if ask_yes_no("Freeze this account? (y/n): "):
            account["status"] = "Frozen"
            print("✔ Account is now FROZEN.")
        else:
            print("Cancelled. No changes made.")
    else:  # frozen
        # frozen -> closed (can't undo so we ask first)
        if ask_yes_no("Close this account permanently? (y/n): "):
            account["status"] = "Closed"
            print("✔ Account is now CLOSED.")
        else:
            print("Cancelled. No changes made.")


#  module menu
# main menu calls this: accounts(staff/role)
# staff is the logged in staff info from the login (has the role inside)
def accounts(staff):
    global current_role
    current_role = staff["role"]    # save the role so we know who is logged in
    running = True
    while running:                  # keeps showing the menu until they pick return
        print_main_menu_account_management()
        print_divider()
        choice = input("Select an option: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            view_account()
        elif choice == "3":
            print("Work in progress...")
        elif choice == "4":
            freeze_or_close_account(staff)
        elif choice == "5":
            # goes back to the main menu
            running = False
        else:
            print("X Invalid option. Please enter 1-4.")