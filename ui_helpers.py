#Purpose of this file is for anything design related needed by the whole file

ui_design_width = 50

def print_header(title):
    """Print a centered title between two divider lines."""
    print("=" * ui_design_width)
    print(title.center(ui_design_width))
    print("=" * ui_design_width)

def print_divider():
    """Print a single divider line."""
    print("-" * ui_design_width)

def print_main_menu():
    """Print the main menu options."""
    print_header("MAIN MENU")
    print("1. Account Management")
    print("2. Deposit / Withdrawal")
    print("3. Fund Transfer")
    print("4. Statements and Interest")
    print("5. Reports & Persistence (Manager only)")
    print("6. Log Out")

def print_main_menu_account_management():
    """Prints full main menu for account management module"""
    print_header("SecureBank - Account Management")
    print("1. Create New Account")
    print("2. View Account Details")
    print("3. Search Accounts")
    print("4. Freeze / Close Account")
    print("5. Return to Main Menu")

def print_main_menu_deposit_withdrawal():
    """Prints full main menu for deposit withdrawal module"""
    print_header("SecureBank - Deposit / Withdrawal")
    print("1. Deposit")
    print("2. Withdrawal")
    print("3. Return to Main Menu")