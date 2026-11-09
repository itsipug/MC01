# SecureBank - Module 1: Account Management (Milestone 1)
# - make one account (savings, checking, or time deposit)
# - view the account
# - manager can freeze then close it

from datetime import date, timedelta   # for the maturity date
from ui_helpers import print_main_menu_account_management, print_divider
# account variables
# these are global - module 2 uses them too

current_role = ""          # set by accounts(role)
has_account = False        # no account until we make one
acc_number = ""
holder_name = ""
acc_type = ""              # Savings / Checking / TimeDeposit
balance = 0.0
status = ""                # Active -> Frozen -> Closed
interest_rate = 0.0
min_balance = 0.0          # savings only
overdraft_limit = 0.0      # checking only
term_days = 0              # time deposit only
maturity_date = ""         # time deposit only, like "2026-11-16"

# account number = branch code + sequence
BRANCH_CODE = "BR01"
next_sequence = 234        # next number to give out

# rules (capital letters so they're easier to change)
SAVINGS_RATE = 2.5
SAVINGS_MIN_BALANCE = 500.0
CHECKING_OVERDRAFT_LIMIT = 5000.0
TIME_DEPOSIT_MIN = 1000.0  # our own rule, brief doesn't say


# ---------- helper functions ----------
def is_valid_amount(text):
    # checks if the input is a positive number like 500 or 500.75
    text = text.strip()
    if text == "":
        return False
    # remove one dot then check if only digits are left
    # this blocks letters, negatives, and stuff like 1.2.3
    if text.replace(".", "", 1).isdigit() == False:
        return False
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


# ---------- input functions ----------
# all of these loop until the input is valid so it never crashes

def ask_account_type():
    while True:
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


# ---------- 1. create account ----------
def create_account():
    # need global so we can change the variables at the top
    global has_account, acc_number, holder_name, acc_type, balance, status
    global interest_rate, min_balance, overdraft_limit, term_days, maturity_date

    # only one acc at a time (ok if the old one is closed)
    if has_account and status != "Closed":
        print("X An active account already exists. Only one account is allowed")
        print("  at a time. Close it first.")
        return

    name = input("Enter account holder name: ").strip()
    if name == "":
        print("X Name cannot be empty. Try again!")
        return

    chosen_type = ask_account_type()

    #  only save them at the end so nothing gets half saved if the user quits
    new_term = 0
    new_maturity = ""
    if chosen_type == "Savings":
        new_rate = SAVINGS_RATE
        new_min = SAVINGS_MIN_BALANCE
        new_overdraft = 0.0
        opening_minimum = SAVINGS_MIN_BALANCE     # has to open with at least 500
    elif chosen_type == "Checking":
        new_rate = 0.0                            # no interest for checking
        new_min = 0.0
        new_overdraft = CHECKING_OVERDRAFT_LIMIT
        opening_minimum = 0.01                    # any amount is ok as long as its more than 0.01
    else:  # time deposit
        new_term = ask_term()
        new_rate = get_time_deposit_rate(new_term)
        new_min = 0.0
        new_overdraft = 0.0
        opening_minimum = TIME_DEPOSIT_MIN
        # today + the term = maturity date
        new_maturity = str(date.today() + timedelta(days=new_term))

    # initial deposit
    deposit = ask_initial_deposit(opening_minimum)

    # all valid, now we save everything
    holder_name = name
    acc_type = chosen_type
    balance = deposit
    status = "Active"                 # new accounts always start active
    interest_rate = new_rate
    min_balance = new_min
    overdraft_limit = new_overdraft
    term_days = new_term
    maturity_date = new_maturity
    acc_number = make_account_number()
    has_account = True

    print("✔ Account created successfully!")
    print(f"Account Number: {acc_number}")
    if acc_type == "TimeDeposit":
        print(f"Type: Time Deposit ({term_days}-day term, matures {maturity_date})")
        print(f"Interest Rate: {interest_rate:.2f}% ({term_days}-day tier)")
    elif acc_type == "Savings":
        print("Type: Savings")
        print(f"Interest Rate: {interest_rate:.2f}%")
    else:
        print("Type: Checking")
        print(f"Overdraft Limit: PHP {overdraft_limit:,.2f}")
    print(f"Balance: PHP {balance:,.2f}")

# ---------- 2. view account ----------
# only reads the variables, doesn't change anything
def view_account():
    if has_account == False:
        print("X No account exists yet. Create one first.")
        return

    print_divider()
    print("ACCOUNT DETAILS")
    print_divider()
    # shown for all types
    print(f"Account Number : {acc_number}")
    print(f"Holder Name    : {holder_name}")
    if acc_type == "TimeDeposit":
        print("Account Type   : Time Deposit")   # space is just for display
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


# ---------- 3. freeze / close (manager only) ----------
# Active -> Frozen -> Closed, one step each time
def freeze_or_close_account():
    global status

    # check the role first, before anything else
    if current_role != "MANAGER":
        print("X ACCESS DENIED: Freezing/closing accounts requires Branch Manager privileges.")
        return

    if has_account == False:
        print("X No account exists yet.")
        return

    # make sure it's the right account
    entered = input("Enter account number: ").strip().upper()
    if entered != acc_number:
        print("X Account not found.")
        return

    print(f"Current status: {status}")

    if status == "Closed":
        print("X This account is already closed.")
    elif status == "Active":
        # active -> frozen
        if ask_yes_no("Freeze this account? (y/n): "):
            status = "Frozen"
            print("✔ Account is now FROZEN.")
        else:
            print("Cancelled. No changes made.")
    else:  # frozen
        # frozen -> closed (can't undo so we ask first)
        if ask_yes_no("Close this account permanently? (y/n): "):
            status = "Closed"
            print("✔ Account is now CLOSED.")
        else:
            print("Cancelled. No changes made.")


# ---------- module menu ----------
# main menu calls this: accounts(role)
# role is "TELLER" or "MANAGER" from the login
def accounts(role):
    global current_role
    current_role = role
    running = True
    while running:
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
            freeze_or_close_account()
        elif choice == "5":
            # goes back to the main menu
            running = False
        else:
            print("X Invalid option. Please enter 1-4.")