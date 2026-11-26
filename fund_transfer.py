
import random
from datetime import date

import account_management as acct
from ui_helpers import print_main_menu_fund_transfer, print_divider,print_error

interbank_fee = 25.0

# daily limits just made up our own limits per accounts
daily_transfer_limits = {
    "Savings": 50000.0,
    "Checking": 100000.0,
    "TimeDeposit": 50000.0,
}

# running total sent this session, keyed by account number
# keyed by number so it already works once there are many accounts
daily_transferred = {}

# every successful transfer is saved as a tuple, module 4 will read these later
# (date, account number, type, amount, balance after)
transactions = []     # TODO: replace with the shared transaction list


# ---------- module menu ----------
def fund_transfer():
    running = True
    while running:
        print_main_menu_fund_transfer()
        print_divider()
        choice = input("Select an option: ").strip()


        match choice:
            case "1":
                internal_transfer()
            case "2":
                external_transfer()
            case "3":
                break
            case _:
                print_error("Invalid choice.")



# ---------- transfers ----------
def internal_transfer():
    if ask_valid_sender() == False:
        return
    # TODO when there are 2+ accounts: ask receiver, look it up, check_status on it,
    # reject sender == receiver, show the receiver's holder name to verify,
    # then move the money with fee 0 (both balances change, so snapshot both for rollback)
    print("Internal transfer needs a second account. Waiting for multi-account support.")


def external_transfer():
    if ask_valid_sender() == False:
        return

    #Asks User for details
    bank_name = input("Enter receiving bank name: ").strip()
    receiver_number = input("Enter receiving account number: ").strip()
    receiver_name = input("Enter receiving account holder name: ").strip()

    if bank_name == "" or receiver_number == "" or receiver_name == "":
        print_error("All receiving details are required.")
        return

    amount = ask_transfer_amount()
    if amount is None:
        return

    # run every check BEFORE touching the balance
    # lowest allowed balance: savings = 500, checking = -5000, time deposit = 0
    floor = acct.min_balance - acct.overdraft_limit
    ok, message = check_funds(acct.balance, floor, amount, interbank_fee)
    if ok == False:
        reject_transfer(message)
        return

    limit = daily_transfer_limits[acct.acc_type]
    already_sent = daily_transferred.get(acct.acc_number, 0.0)
    ok, message = check_daily_limit(limit, already_sent, amount)
    if ok == False:
        reject_transfer(message)
        return

    # recipient verification step
    print_divider()
    print(f"Bank:    {bank_name}")
    print(f"Account: {receiver_number}")
    print(f"Name:    {receiver_name}")
    print(f"Amount:  PHP {amount:,.2f}")
    print(f"Fee:     PHP {interbank_fee:.2f}")
    print_divider()
    if acct.ask_yes_no("Confirm transfer? (y/n): ") == False:   # reusing your y/n helper
        print("Transfer cancelled.")
        return

    if apply_external_transfer(amount, interbank_fee) == False:
        reject_transfer("Transfer failed unexpectedly.")
        return

    transactions.append((str(date.today()), acct.acc_number, "Transfer", amount, acct.balance))
    print(f"✔ Transfer successful. Reference number: {make_reference_number()}")
    print(f"New balance: PHP {acct.balance:,.2f}")


# ---------- helpers ----------

def reject_transfer(message):
    # used when a check fails before any money moved
    print_error(message)
    print("Transaction rolled back; no changes were made.")


def ask_transfer_amount():
    # returns the amount as a float, or None if the input was invalid
    text = input("Enter amount to transfer: ").strip()
    if acct.is_valid_amount(text) == False:        # reusing your validator from module 1
        print_error("Invalid amount. Enter a positive number.")
        return None
    return round(float(text), 2)


def make_reference_number():
    return f"IB{date.today():%Y%m%d}{random.randint(1000, 9999)}"


def ask_valid_sender():
    # asks for the sender and runs the checks EVERY transfer needs
    # returns True if the account may send money, False if not (error already printed)
    if acct.has_account == False:
        print_error("No account exists yet. Create one first.")
        return False

    account_number = input("Enter sender account number: ").strip().upper()
    if account_number != acct.acc_number:
        print_error("Sender account not found.")
        return False

    ok, message = check_status(acct.status)
    if ok == False:
        print_error(message)
        return False

    ok, message = check_time_deposit(acct.acc_type, acct.maturity_date)
    if ok == False:
        print_error(message)
        return False

    return True


def apply_external_transfer(amount, fee):
    # the only place that changes numbers. Two things change (balance + daily total),
    # so if the second one fails we undo the first. Returns True if it worked.
    old_balance = acct.balance
    old_daily = daily_transferred.get(acct.acc_number, 0.0)
    try:
        acct.balance = acct.balance - amount - fee
        daily_transferred[acct.acc_number] = old_daily + amount
        return True
    except TypeError:                      # e.g. a balance that isn't a number
        acct.balance = old_balance
        daily_transferred[acct.acc_number] = old_daily
        return False






# ---------- checks ----------
# these take plain values (not acct.something) so they never need to change
# when the account storage changes. Each returns (ok, error_message)

#Checks if account is active
def check_status(status):
    if status != "Active":
        return False, f"This account is {status}. Only Active accounts can transfer."
    return True, ""

#Checks if account is a timedeposit and if its transferring before maturity date
def check_time_deposit(acc_type, maturity_date):
    if acc_type == "TimeDeposit":
        if date.today() < date.fromisoformat(maturity_date):
            return False, "Cannot transfer from a Time Deposit account before maturity."
    return True, ""


#Checks if accounts will reach overdraft limit (hey wait isnt overdraft only for checking?)
#Checks if after transfer would leave the balance with negative
def check_funds(balance, floor, amount, fee):
    # floor = the lowest balance the account is allowed to reach
    if balance - amount - fee < floor:
        if floor < 0:
            limit_name = "overdraft limit"
        else:
            limit_name = "minimum balance"
        if fee > 0:
            return False, (f"Insufficient funds. Interbank transfer fee (PHP {fee:.2f}) "
                           f"would push this account below its {limit_name}.")
        return False, f"Insufficient funds. This would push the account below its {limit_name}."
    return True, ""


def check_daily_limit(limit, already_sent, amount):
    if already_sent + amount > limit:
        remaining = limit - already_sent
        return False, (f"Daily transfer limit of PHP {limit:,.2f} exceeded. "
                       f"Remaining today: PHP {remaining:,.2f}.")
    return True, ""


