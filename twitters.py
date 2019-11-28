import tweepy
import webbrowser
from keys import twitter_creds as keys
from datetime import datetime


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
            print(f"[*] You are now logged in as {api.me().name} (@{api.me().screen_name})")
            break
        except tweepy.error.TweepError:
            print("[!] Error, pin not valid, please re-enter.")

    return api


def rate_limit_check(api):
    rate_limit = api.rate_limit_status()["resources"]
    for rate in rate_limit:
        endpoints = rate_limit[rate]
        for endpoint in endpoints:
            limit = rate_limit[rate][endpoint]["limit"]
            remaining = rate_limit[rate][endpoint]["remaining"]
            if remaining == 0:
                print(f"[!] Rate limit hit for {rate}:{endpoint}, max limit is {limit}, ")
            elif limit > remaining:
                print(f"[-] {remaining}/{limit} calls remaining for {rate}:{endpoint}")


def check_if_account_is_active(api, a):
    while True:
        try:
            u = api.get_user(a)
            print(f"[*] Account {a} still exists")
            return True
        except tweepy.error.RateLimitError:
            resume_time = (datetime.now() + timedelta(minutes=15)).strftime("%I:%M:%S %p")
            print(
                f"[!] Potential rate limit hit for an endpoint, initiating 15-minute pause, will resume at {resume_time}")
            rate_limit_check(api)
            time.sleep(60 * 15)
        except tweepy.error.TweepError as e:
            error_message = e.args[0][0]["message"]
            print(f"[!] Error: {error_message}")
            return False
