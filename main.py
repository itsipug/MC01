#Importing of modules
from login_access_control import *
from account_management import *
from depositing_withdrawal import *

width = 40

print("="*40)
print("Secure Bank - Staff Login".center(width))
print("="*40)

result = login()

#Is none meaning failed
if result is None:
    print("Too many failed attempts, try again later!")
else:
    staff_name, role = result

    if role == "Branch Manager":
        print("Access: transactions, freezing/closing accounts, reports")
    else:
        print("Access: transactions only")

