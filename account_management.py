from ui_helpers import print_divider, print_main_menu_account_management

#Sample account
accounts = {
    "BR01-00001": {
        "holder": "Maria Santos",
        "type": "Savings",             # Savings / Checking / TimeDeposit
        "balance": 5000.00,
        "status": "Active",            # Active / Frozen / Closed
        "term_days": None,             # only used by TimeDeposit
        "maturity_date": None,         # only used by TimeDeposit, e.g. "2026-11-16"
    },
}


def accounts_management():
    """Main Menu of accounts management/ what the user sees upon selecting accounts management"""

    while True:
        print_main_menu_account_management()
        print_divider()
        choice = input("Select an option: ").strip()

        match choice:
            case "1":
                print("Making new account or something") #
                account_type = ask_account_type()
                if account_type == "TimeDeposit":
                    term_days = ask_term()
                initial_deposit = ask_initial_deposit()
                print(account_type, term_days, initial_deposit)
            case "5":
                break #This returns the user back to the main menu


def ask_account_type():
    while True:
        account_type = input("Enter account type (Savings/Checking/TimeDeposit): ").strip()
        normalized = account_type.lower().replace(" ", "")
        if account_type == "Savings":
            return "Savings"
        elif account_type == "Checking":
            return "Checking"
        elif account_type == "TimeDeposit" or account_type == "time deposit" or account_type == "Time Deposit":
            return "TimeDeposit"
        else:
            print("X INVALID CHOICE. Try again")

def ask_term():
    while True:
        deposit_term = input("Enter deposit term (30/60/90 days):  ").strip()
        if deposit_term == "30" or deposit_term == "60" or deposit_term == "90":
            return int(deposit_term)
        print("X Term must be 30, 60, or 90. Try again!")

def ask_initial_deposit():
    while True:
        initial_deposit_amount = int(input("Enter initial deposit amount: "))
        return initial_deposit_amount
