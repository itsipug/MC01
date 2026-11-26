from ui_helpers import print_main_menu_statements, print_divider, print_error
import account_management as acct

# TEMP: fake transactions for testing, delete when the shared list exists
# row shape: (date, account number, type, amount, balance after)
# BR01-00234 = Maria Santos, Savings    BR01-00235 = Roberto Cruz, Checking
transactions = [
    ("2026-06-02", "BR01-00234", "Deposit",    20000.00, 20000.00),
    ("2026-06-15", "BR01-00234", "Withdrawal",  3000.00, 17000.00),
    ("2026-06-30", "BR01-00234", "Interest",      35.42, 17035.42),
    ("2026-07-05", "BR01-00234", "Deposit",     8000.00, 25035.42),
    ("2026-07-12", "BR01-00234", "Transfer",    5000.00, 20010.42),   # 5,000 + 25 fee left the account
    ("2026-07-31", "BR01-00234", "Interest",      41.69, 20052.11),
    ("2026-08-03", "BR01-00234", "Withdrawal",  1500.00, 18552.11),
    ("2026-08-20", "BR01-00234", "Deposit",    12000.00, 30552.11),
    ("2026-08-31", "BR01-00234", "Interest",      63.65, 30615.76),
    ("2026-09-01", "BR01-00235", "Deposit",     5000.00,  5000.00),
    ("2026-09-10", "BR01-00234", "Transfer",   10000.00, 20590.76),   # 10,000 + 25 fee
    ("2026-09-15", "BR01-00235", "Withdrawal",  7000.00, -2050.00),   # overdraft, includes the 50 fee
    ("2026-09-30", "BR01-00234", "Interest",      42.90, 20633.66),
    ("2026-10-01", "BR01-00235", "Deposit",     4000.00,  1950.00),
    ("2026-10-08", "BR01-00234", "Withdrawal",  2500.00, 18133.66),
    ("2026-10-25", "BR01-00234", "Deposit",     6000.00, 24133.66),
    ("2026-10-31", "BR01-00234", "Interest",      50.28, 24183.94),
    ("2026-11-05", "BR01-00235", "Transfer",    1000.00,   925.00),   # 1,000 + 25 fee
    ("2026-11-12", "BR01-00234", "Transfer",    3000.00, 21158.94),   # 3,000 + 25 fee
    ("2026-11-20", "BR01-00234", "Withdrawal",   800.00, 20358.94),
]




def statements_interests():
   while True:
        print_main_menu_statements()
        print_divider()

        choice = input("Enter your choice: ").strip()

        match choice:
            case "1":
                view_statements()
            case "2":
                print("Run monthly interests posting selected")
            case "3":
                break
            case _:
                print("Invalid Choice")


#Todo: I think this code can be cleaned up with more helper functions
def view_statements():

    #Check if there's a created account
    if acct.has_account == False:
        print_error("Account not found")
        return


    account_number = input("Enter account number: ").strip().upper()

    #Does account number given match active account?
    if account_number != acct.acc_number:
        print_error("Account not found")
        return


    account_rows = [] #A list where the filtered out transactions will go based on account number
    for transaction in transactions:
        if account_number == transaction[1]:
            account_rows.append(transaction)

    valid_types = ("Deposit", "Withdrawal", "Transfer", "All")

    while True:
        chosen_type = input("Filter by type (Deposit/Withdrawal/Transfer/All): ").strip().title()
        if chosen_type in valid_types: #Checks if type inputted by user matches with valid types
            break
        print_error("Invalid Type")

    shown_rows = [] #Where account_rows will be appended to after filtering by type
    for row in account_rows:
        if chosen_type == "All" or row[2] == chosen_type:
            shown_rows.append(row)

    #Printing of rows
    recent_rows = shown_rows[-10:]
    if len(shown_rows) == 0:
        print("No transactions found.")
        return
    print(f"--- Statement: {acct.acc_number} ({acct.holder_name}) - Showing {len(recent_rows)} of {len(shown_rows)} ---")
    print(f"{'Date':<12}{'Type':<12}{'Amount':>14}{'Balance After':>16}")  # once, above the loop
    print("-"*54)
    for row_date, number, kind, amount, balance_after in recent_rows:
        print(f"{row_date:<12}{kind:<12}{amount:>14,.2f}{balance_after:>16,.2f}")


def monthly_interests_post():
    while True:
        pass