# GetYourName

This script automatically checks if a list of usernames are available on Twitter and sends you an email when one becomes available.

Set Up:

In run.py, set recipient to the email address you want to receive alerts.

Create the file credentials.json with the following two template:
```bash
{
  "twitter_creds": {
    "TWITTER_CONSUMER_KEY": "",
    "TWITTER_CONSUMER_SECRET": "",
    "TWITTER_ACCESS_KEY": "",
    "TWITTER_ACCESS_SECRET": ""
  },
  "email_login": {
    "user": "",
    "pass": ""
  }
}

```

You can create a Twitter app and get API keys [here](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens)

I am using a Gmail account for sending emails, set up instructions [here](https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/)
