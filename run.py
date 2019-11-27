#######################
import tweepy
import webbrowser
from keys import *

accounts_file_name = "accounts.txt"


"""
TWITTER ACCOUNT API INTERACTIONS
"""


def twitter_account_login():
    print("[*] Opening web browser. Login to target Twitter account and copy PIN.")

    api_key = keys["API_KEY"]
    api_key_secret = keys["API_KEY_SECRET"]

    auth = tweepy.OAuthHandler(api_key, api_key_secret)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print("[!] Error, failed to get request token.\n"
              "...goodbye...")
        quit()

    webbrowser.open(redirect_url)

    while True:
        try:
            pin = input("[?] Enter pin: ").strip()
            token = auth.get_access_token(verifier=pin)
            access_token = token[0]
            access_token_secret = token[1]
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth, wait_on_rate_limit_notify=True)
            break
        except tweepy.error.TweepError:
            print("[!] Error, pin not valid, please re-enter.")

    return api



def check_if_account_is_active(a):
    pass


"""
FILE I/O
"""


def open_accounts_file():
    with open(accounts_file_name, 'w+') as f:
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
    api = twitter_account_login()
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
            # Add account
        elif selection == 'd':
            # delete account

    print("[*] Saving current list of tracked accounts...")
    save_accounts_file(current_accounts_to_check)

