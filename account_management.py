def accounts():
    print("Hi from account management")

def line(char="=", length=50):
    print(char * length)


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
