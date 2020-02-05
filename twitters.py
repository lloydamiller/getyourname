import tweepy
from datetime import datetime, timedelta
import time
import json


class Twitter:

    def __init__(self):

        with open("credentials.json", 'r') as f:
            keys = json.load(f)["twitter_creds"]

        twitter_api = keys["TWITTER_CONSUMER_KEY"]
        twitter_api_secret = keys["TWITTER_CONSUMER_SECRET"]
        twitter_api_access = keys["TWITTER_ACCESS_KEY"]
        twitter_api_access_secret = keys["TWITTER_ACCESS_SECRET"]

        auth = tweepy.OAuthHandler(twitter_api, twitter_api_secret)
        auth.set_access_token(twitter_api_access, twitter_api_access_secret)
        self.api = tweepy.API(auth)

    def rate_limit_check(self):
        rate_limit = self.api.rate_limit_status()["resources"]
        for rate in rate_limit:
            endpoints = rate_limit[rate]
            for endpoint in endpoints:
                limit = rate_limit[rate][endpoint]["limit"]
                remaining = rate_limit[rate][endpoint]["remaining"]
                if remaining == 0:
                    print(f"[!] Rate limit hit for {rate}:{endpoint}, max limit is {limit}, ")
                elif limit > remaining:
                    print(f"[-] {remaining}/{limit} calls remaining for {rate}:{endpoint}")

    def check_if_account_is_active(self, a):
        while True:
            try:
                u = self.api.get_user(a)
                print(f"[*] Account {a} still exists")
                return True
            except tweepy.error.RateLimitError:
                resume_time = (datetime.now() + timedelta(minutes=15)).strftime("%I:%M:%S %p")
                print(
                    f"[!] Potential rate limit hit for an endpoint, initiating 15-minute pause, will resume at {resume_time}")
                self.rate_limit_check()
                time.sleep(60 * 15)
            except tweepy.error.TweepError as e:
                error_message = e.args[0][0]["message"]
                print(f"[!] Error: {error_message}")
                return False
