from ui_helpers import print_header

#Initializing Variables
max_attempts = 3
staff_credentials = {
    "teller": {"name": "Adrian Serrano", "password": "admin123", "role": "TELLER"},
    "ihatemanagers321": {"name": "John Doe", "password": "321admin", "role": "BRANCH MANAGER"}
}


def login():

    """
    Show the login screen and allow up to max_attempts tries.
    Returns the matching staff record (dict) on success,
    or None if the user is locked out.
    """

    print_header("SecureBank - Staff Login")

    for attempt in range(1, max_attempts+1 ):
        # .strip() for avoiding trailing spaces leading to failed login
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ")

        staff = staff_credentials.get(username)
        if staff is not None and staff["password"] == password:
            print("Login Successful!")
            print(f"Welcome, {staff['name']} - Role: {staff['role']}")
            return staff

        print(f"Incorrect Username or Password. Attempt {attempt} of {max_attempts}")

    print("Too many failed attempts. Access will be locked for this session ")
    return None

def is_branch_manager(staff):
    """Return True if this staff record has the BRANCH MANAGER role."""
    return staff["role"] == "BRANCH MANAGER"

def requires_manager(staff):
    """Gatekeeper for manager-only actions.

    Returns True if allowed. Otherwise, prints a denial and returns False,
    so callers can just do: if not requires_manager(staff): return
    """
    if is_branch_manager(staff):
        return True
    print("ACCESS DENIED: This action requires Branch Manager privileges.")
    return False
