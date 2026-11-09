def accounts():
    print("Hi from account management")

def line(char="=", length=50):
    print(char * length)

current_role = ""
has_account = False
acc_holder = ""
holder_name = ""
acc_type = ""
balance = 0.0
status = ""
interest_rate = 0.0
min_balance = 0.0
term_days = 0
maturity_days = 0

BRANCH_CODE = "BRANCH 1"
next_sequence = 234

savings_rate = 2.5
savings_min_balance = 500.0
checking_overdraft_limit = 5000.0
time_deposit_min = 1000.0

def is_valid_amount(text):
    text = text.strip()
    if text == "":
        return False
    if text.replace(".", "", 1).isdigit() == False:
        return False
    if float(text) <= 0:
        return False
    return True

def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer == "yes":
            return True
        if answer == "no":
            return False
        print("X Please type yes or no.")


def make_account_number():
    global next_sequence
    number = (f"{BRANCH_CODE}-{next_sequence:05d}")
    next_sequence = next_sequence + 1
    return number


def get_time_deposit_rate(days):
    if days == 30:
        return 3.25
    elif days == 60:
        return 4.00
    else: # FOR 90 DAYS
        return 4.75


# INPUT FUNCTIONS
def ask_account_type():
    while True:
        text = input("Enter account type (Savings/Checking/TimeDeposit): ").strip()
        if text == "Savings":
            return "Savings"
        elif text == "Checking":
            return "Checking"
        elif text == "TimeDeposit" or text == "time deposit" or text == "Time Deposit":
            return "Time Deposit"
        else:
            print("X INVALID CHOICE. Try again")

def ask_term():
    while True:
        text = input("Enter deposit term (30/60/90 days):  ").strip()
        if text == "30" or text == "60" or text == "90":
            return int(text)
        print("X Term must be 30, 60, or 90. Try again!")

def ask_initial_deposit():
    while True:
        text = input("Enter initial deposit amount: ").strip()
        if is_valid_amount(text) == False:
            print("X INVALID AMOUNT. Try again!")
        elif float(text) < minimum:
            print(f"X INVALID AMOUNT. Try again! {minimum:,.2f}.")

def create_account():
    global has_account, acc_number, holder_name, acc_type, balance, status
    global interest_rate, min_balance, overdraft_limit, term_days, maturity_date

    # only one acc at a time
    if has_account and status != "Closed":
        print("X An active account already exists. Only one account is allowed at a time. Close it first.")
        return

    name = input("Enter account name: ").strip()
    if name == "":
        print("Name cannot be empty. Try again!")
        return

    chosen_type = ask_account_type()

    new_term = 0
    new_maturity = ""
    if chosen_type == "Savings":
        new_rate = SAVINGS_RATE
        new_min = SAVING_MIN_BALANCE
        new_overdraft = 0.0
        opening_minimum = SAVINGS_MIN_BALANCE
    elif chosen_type == "Checking":
        new_rate = 0.0
        new_min = 0.0
        new_overdraft = CHECKING_OVERDRAFT_LIMIT
        opening_minimum = 0.01
    else: # Time deposit
        new_term = ask_term()
        new_rate = get_time_deposit_rate(new_term)
        new_min = 0.0
        new_overdraft = 0.0
        opening_minimum = TIME_DEPOSIT_MIN
        new_maturity = str(date.today() + timedelta(days=new_term))

    #initial deposit
    deposit = ask_initial_deposit(opening_minimum)
