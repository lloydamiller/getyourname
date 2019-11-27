#######################


accounts_file_name = "accounts.txt"

def open_accounts_file():
    with open("", 'w+') as f:
        t = f.read()
        if len(t) == 0:
            print("[!] This bot is not listening for any accounts, please add one to contunue")
            return []
        else:
            return t.split(",")

###


if __name__ == "__main__":
    print("WELCOME TO THE TWITTER ACCOUNT LISTENER")
    current_accounts_to_check = open_accounts_file()