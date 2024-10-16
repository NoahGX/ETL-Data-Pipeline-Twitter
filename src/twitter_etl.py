import os
import s3fs
import json
import tweepy
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Use environment variable for API Key storage
load_dotenv(dotenv_path='../config/.env')

def run_twitter_etl():
    access_key = os.getenv('ACCESS_KEY')
    access_secret = os.getenv('ACCESS_SECRET')
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')

    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    # Create the API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            # Set maximum count allowed
                            count=200,
                            include_rts = False,
                            # Necessary to keep full text 
                            tweet_mode = 'extended')

    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        list.append(refined_tweet)

    df = pd.DataFrame(list)
    df.to_csv('../data/refined_tweets.csv', index=False)