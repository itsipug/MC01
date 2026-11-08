from login_access_control import login,requires_manager
from account_management import accounts_management
from ui_helpers import print_divider, print_main_menu

current_staff = login()

if current_staff is not None:
    while True:

        print_main_menu()
        print_divider()
        choice = input("Select an option: ").strip()

        match choice:
            case "1":
                #Brings user over to accounts management and everything is handled separately in accounts management
                accounts_management()
            case "2":
                #Call future module here change this once done
                print("Work in progress...")
            case "3":
                #Call future module here change this once done
                print("Work in progress...")
            case "4":
                #Call future module here change this once done
                print("Work in progress...")
            case "5":
                #Checks if user is branch manager otherwise is restricted from access
                if requires_manager(current_staff):
                    print("Sup manager")
                    print("check this out")
            case "6":
                print("Logging out....")
                break
            case _:
                print("Invalid option")




