import os
import s3fs
import tweepy
import pandas as pd
from dotenv import load_dotenv

# Use environment variable for API Key storage
load_dotenv(dotenv_path='../config/.env')

def run_twitter_etl():
    access_key = os.getenv('ACCESS_KEY')
    access_secret = os.getenv('ACCESS_SECRET')
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')

    # Twitter authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Create the API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(
        screen_name='@elonmusk', 
        count=200,
        include_rts = False,
        tweet_mode = 'extended'
    )

    tweet_list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {
            "user": tweet.user.screen_name,
            'text' : text,
            'favorite_count' : tweet.favorite_count,
            'retweet_count' : tweet.retweet_count,
            'created_at' : tweet.created_at
        }

        tweet_list.append(refined_tweet)
        
    # Save the data to the data directory
    df = pd.DataFrame(tweet_list)
    df.to_csv('s3://etl-data-pipeline-twitter/refined_tweets.csv', index=False)