staff_accounts = {
    "teller01":{
        "password":"pass123",
        "name":"Maria Santos",
        "role":"Teller"
    },
    "manager01":{
        "password":"admin456",
        "name":"Jose Reyes",
        "role":"Branch Manager"
    },

}
maximum_login_attempts = 3

def login():
    login_attempts = 0
    while login_attempts < maximum_login_attempts:
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        #Fetches staff account details using username
        account = staff_accounts.get(username)

        #Checks if account exists if not it becomes none and if yes it becomes an account
        #Checks password associated with account with user inputted password
        if account is not None and account["password"] == password:
            print(f"\nWelcome, {account['name']}! Role: {account['role']}")
            return account["name"], account["role"]


        login_attempts = login_attempts + 1
        remaining_attempts = maximum_login_attempts - login_attempts
        print(f"Invalid Credentials: {remaining_attempts} attempt(s) out of 3 remaining")
    return None