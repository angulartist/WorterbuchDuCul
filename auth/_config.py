import tweepy as tpy

profile = {
    "consumer_key": "",
    "consumer_secret": "",
    "access_token": "",
    "access_token_secret": "",
}

def init_api():
    auth = tpy.OAuthHandler(profile["consumer_key"], profile["consumer_secret"])
    auth.set_access_token(profile["access_token"], profile["access_token_secret"])
    
    return tpy.API(auth)
