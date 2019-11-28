#######################
import twitters
from alert import send_alert_by_email
import time

accounts_file_name = "accounts.txt"
recipient = "lloydamiller@me.com" # email address where you want

"""
FILE I/O
"""


def open_accounts_file():
    with open(accounts_file_name, 'r+') as f:
        t = f.read()
        if len(t) == 0:
            print("[!] This bot is not listening for any accounts, please add one to contunue")
            return []
        else:
            return t.split(",")


def save_accounts_file(d):
    d = ','.join(d)
    with open(accounts_file_name, 'w+') as f:
        f.write(d)


if __name__ == "__main__":
    print("WELCOME TO THE TWITTER ACCOUNT LISTENER")
    print("Please connect to an active Twitter account for using API")
    api = twitters.twitter_account_login()
    current_accounts_to_check = open_accounts_file()
    if len(current_accounts_to_check) == 0:
        print("[*] Please add at least one account name")
        account = input("[?] Username: ")
        current_accounts_to_check.append(account)
    while True:
        print(f"[*] Current Accounts Tracked:")
        for tracked_account in current_accounts_to_check:
            print(f"    0{current_accounts_to_check.index(tracked_account)+1}. @{tracked_account}")

        print("""
[*] Options: 
    (a)dd an account to track
    (d)elete a tracked account
    (b)egin tracking""")
        selection = input("[?] What would you like to do? ").lower()

        if selection not in ['a','d','b']:
            continue

        elif selection == 'b':
            break

        elif selection == 'a':
            print("[*] Enter the user name (not including @) of the account you want to track")
            new_user = input("[?] Enter username: ")
            if new_user not in current_accounts_to_check:
                current_accounts_to_check.append(new_user)
            continue

        elif selection == 'd':
            print("[*] Enter the number for the account you want removed")
            position = int(input("[?] Number: "))-1
            confirm_delete = input(f"[?] Are you sure you want to stop tracking {current_accounts_to_check[position]} (y/n) ")
            if confirm_delete == 'y':
                del current_accounts_to_check[position]
            continue

    print("[*] Saving current list of tracked accounts...")
    save_accounts_file(current_accounts_to_check)

    while len(current_accounts_to_check) > 0:
        print("")
        print("[*] Checking if accounts exist...")
        print(f"[*] Accounts tracked:")
        for tracked_account in current_accounts_to_check:
            print(f"    0{current_accounts_to_check.index(tracked_account)+1}. @{tracked_account}")

        for account in current_accounts_to_check:
            test = twitters.check_if_account_is_active(api, account)
            if test is False:
                print(f"[!] Account {account} could be available!")
                print(f"    Sending email to {recipient} now...")
                email_subject = f"ALERT: @{account} Could Be Available Now"
                email_body = "Go to https://twitter.com/signup and register it now!"
                send_alert_by_email(recipient, email_subject, email_body)
                current_accounts_to_check.remove(account)
            time.sleep(5)

        save_accounts_file(current_accounts_to_check)
