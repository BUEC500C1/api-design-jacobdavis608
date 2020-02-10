
import tweepy
KEY_FILEPATH = "../access.txt"
import wget

def twitter_summary():
    tokens = []
    try:
        with open(KEY_FILEPATH, "r") as fp:
            for token in fp.readlines():
                tokens.append(token.rstrip())
    except:
        print("Cannot find Tweepy API keys")
        print("Exiting...")
        return

    access_token, access_token_secret, api_key, api_key_secret = tokens
    
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    public_tweets = api.home_timeline(count=100)
    media_files = set()
    for tweet in public_tweets:
        try:
            media = tweet.entities.get('media', [])
            media_files.add(media[0]['media_url'])
        except:
            continue
    print(len(media_files))


if __name__ == "__main__":
    twitter_summary()