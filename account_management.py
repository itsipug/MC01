def accounts():
    print("Hi from account management")

def line(char="=", length=50):
    print(char * length)


def is_valid_amount(text):
    text = text.strip()
    if text == "":
        return False