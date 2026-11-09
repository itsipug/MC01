from ui_helpers import print_divider,print_main_menu_deposit_withdrawal
import account_management as acct            # acct.balance = the balance variable from module 1


# SecureBank - Module 2: Deposit & Withdrawal (Milestone 1)
# - deposit money
# - withdraw money with the rules for each account type

from ui_helpers import print_divider

OVERDRAFT_FEE = 50.0
LARGE_TRANSACTION = 20000.0    # above this we need to confirm twice

# daily withdrawal limits per account type
# (brief doesn't give numbers so these are ours)
SAVINGS_DAILY_LIMIT = 50000.0
CHECKING_DAILY_LIMIT = 100000.0
TIME_DEPOSIT_DAILY_LIMIT = 200000.0

# running total for the session
withdrawn_today = 0.0          # how much was withdrawn so far
tracked_account = ""           # which account the total is for


# ---------- helper functions ----------
def get_daily_limit():
    # gives the limit based on the account type
    if acct.acc_type == "Savings":
        return SAVINGS_DAILY_LIMIT
    elif acct.acc_type == "Checking":
        return CHECKING_DAILY_LIMIT
    else:
        return TIME_DEPOSIT_DAILY_LIMIT


def select_account():
    # asks for the account number and checks if we can use it
    # returns True if ok, False if we should stop
    # deposit and withdraw both use this so we only write it once
    global withdrawn_today, tracked_account

    # is there an account?
    if acct.has_account == False:
        print("X No account exists yet. Create one in Account Management first.")
        return False

    # does the number match?
    entered = input("Enter account number: ").strip().upper()
    if entered != acct.acc_number:
        print("X Account not found.")
        return False

    # only active accounts can do transactions
    if acct.status == "Frozen":
        print("X ERROR: This account is FROZEN. No transactions allowed.")
        return False
    if acct.status == "Closed":
        print("X ERROR: This account is CLOSED. No transactions allowed.")
        return False

    # if it's a different account than before (new one was made)
    # reset the daily total back to 0
    if tracked_account != acct.acc_number:
        tracked_account = acct.acc_number
        withdrawn_today = 0.0

    return True


def ask_amount(word):
    # word is just for the prompt ("deposit" or "withdrawal")
    # is_valid_amount is from module 1 so we don't write it again
    while True:
        text = input(f"Enter {word} amount: ").strip()
        if acct.is_valid_amount(text):
            return float(text)
        print("X INVALID AMOUNT. Enter a positive number.")


def double_confirm(word, amount):
    # over 20,000 = confirm twice
    # returns True if ok to continue, False if cancelled
    if amount <= LARGE_TRANSACTION:
        return True        # small amount, skip

    print(f"⚠ Large transaction detected (over PHP {LARGE_TRANSACTION:,.0f}). Please confirm twice.")
    # 1st confirm
    if acct.ask_yes_no(f"Confirm {word} of PHP {amount:,.2f}? (y/n): ") == False:
        print("Transaction cancelled by staff.")
        return False
    # 2nd confirm
    if acct.ask_yes_no("Confirm AGAIN to proceed? (y/n): ") == False:
        print("Transaction cancelled by staff.")
        return False
    return True


# ---------- deposit ----------
def deposit():
    # check the account first
    if select_account() == False:
        return

    amount = ask_amount("deposit")

    # confirm twice if it's big
    if double_confirm("deposit", amount) == False:
        return

    # all good, add the money
    acct.balance = acct.balance + amount
    print("✔ Deposit processed.")
    print(f"New balance: PHP {acct.balance:,.2f}")


# ---------- withdrawal ----------
# order of the checks:
# account -> time deposit lock -> amount -> daily limit
# -> balance rules per type -> large confirm -> then change the balance
# balance only changes at the very end after everything passed
def withdraw():
    global withdrawn_today

    if select_account() == False:
        return

    # time deposit lock
    # dates are "YYYY-MM-DD" text so comparing them as text works
    # we check this before asking the amount since it's blocked no matter what
    if acct.acc_type == "TimeDeposit":
        today = str(date.today())
        if today < acct.maturity_date:
            print("X ERROR: This is a Time Deposit account. Withdrawals are locked")
            print(f"  until the maturity date ({acct.maturity_date}).")
            return

    amount = ask_amount("withdrawal")

    # daily limit (add the new amount to what was already withdrawn)
    daily_limit = get_daily_limit()
    if withdrawn_today + amount > daily_limit:
        remaining = daily_limit - withdrawn_today
        print(f"X ERROR: Daily withdrawal limit of PHP {daily_limit:,.2f} would be exceeded.")
        print(f"  Remaining allowance today: PHP {remaining:,.2f}")
        return

    # balance rules per account type
    # uses_overdraft remembers if we need to charge the 50 fee later
    uses_overdraft = False

    if acct.acc_type == "Savings":
        # savings must keep the minimum balance (500)
        if acct.balance - amount < acct.min_balance:
            available = acct.balance - acct.min_balance
            print(f"X ERROR: Savings accounts must keep a minimum balance of PHP {acct.min_balance:,.2f}.")
            print(f"  Maximum you can withdraw now: PHP {available:,.2f}")
            return

    elif acct.acc_type == "Checking":
        # checking can go below zero but only up to the overdraft limit
        if amount > acct.balance:
            # the fee counts too so we subtract it when checking the limit
            balance_after = acct.balance - amount - OVERDRAFT_FEE
            if balance_after < -acct.overdraft_limit:
                print(f"X ERROR: This withdrawal would go past the overdraft limit of PHP {acct.overdraft_limit:,.2f}.")
                return
            # warn first then ask
            print(f"Current balance: PHP {acct.balance:,.2f}")
            print("⚠ This withdrawal exceeds the available balance. Overdraft")
            print(f"  protection will apply a PHP {OVERDRAFT_FEE:.2f} fee.")
            if acct.ask_yes_no("Proceed with overdraft withdrawal? (y/n): ") == False:
                print("Transaction cancelled by staff.")
                return
            uses_overdraft = True

    else:  # time deposit that already matured
        # no overdraft, can't go below zero
        if amount > acct.balance:
            print(f"X ERROR: Insufficient funds. Balance is PHP {acct.balance:,.2f}.")
            return

    # confirm twice if big
    if double_confirm("withdrawal", amount) == False:
        return

    # everything passed so now we change the balance
    acct.balance = acct.balance - amount
    withdrawn_today = withdrawn_today + amount

    if uses_overdraft:
        acct.balance = acct.balance - OVERDRAFT_FEE
        print("✔ Withdrawal processed with overdraft.")
        print(f"New balance: PHP {acct.balance:,.2f} (includes PHP {OVERDRAFT_FEE:.2f} overdraft fee)")
    else:
        print("✔ Withdrawal processed.")
        print(f"New balance: PHP {acct.balance:,.2f}")

    print(f"Withdrawn today: PHP {withdrawn_today:,.2f} of PHP {daily_limit:,.2f} limit")


# ---------- module menu ----------
# main menu calls this: deposit_withdrawal()
def deposit_withdrawal():
    running = True
    while running:
        print_main_menu_deposit_withdrawal()
        print_divider()
        choice = input("Select an option: ").strip()

        if choice == "1":
            deposit()
        elif choice == "2":
            withdraw()
        elif choice == "3":
            running = False    # back to main menu
        else:
            print("X Invalid option. Please enter 1-3.")