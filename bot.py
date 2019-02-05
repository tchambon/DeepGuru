import tweepy
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json
import os


PATH = Path('./data/')
FILE_FROM = PATH/'tweet-from.csv'
FILE_TO = PATH/'tweet-to.csv'

def new_tweet(api, tweet):
    #api.update_status(tweet)
    print(f'PUBLISHING TWEET {tweet}')

def update_tweet_lists(df_from, df_to, index):
    msg = df_from.loc[index, 'text']
    
    df_to = df_to.append({'text': msg, 'publication_date': datetime.datetime.now()}, ignore_index=True)
    df_from = df_from.drop(index=index)

    return df_from, df_to

def execute_new_post(api, df_from, df_to, filename_from, filename_to):
    index_tweet = df_from.index[0]
    content_tweet = df_from.iloc[0].text
    
    df_from, df_to = update_tweet_lists(df_from, df_to, index_tweet)
    new_tweet(api, content_tweet)
    
    update_dataframes_tweet(df_from, df_to, filename_from, filename_to)
    
    return df_from, df_to

def update_dataframes_tweet(df_from, df_to,filename_from, filename_to):
    df_from.to_csv(filename_from)
    df_to.to_csv(filename_to)



with open('data/identifiers/twitter.json', 'r') as f:
        twitter_json = json.load(f)

# Information to connect to twitter API
consumer_key = twitter_json['consumer_key']
consumer_secret = twitter_json['consumer_secret']
access_token = twitter_json['access_token']
access_token_secret = twitter_json['access_token_secret']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

df_from = pd.read_csv(FILE_FROM, index_col=0)

if not os.path.exists(FILE_TO):
    print('File tweet to does not exists: file creation')
    df_create = pd.DataFrame(columns=['text', 'publication_date'])
    df_create.to_csv(FILE_TO)

df_to = pd.read_csv(FILE_TO, index_col=0)

len_before_from = len(df_from)
len_before_to = len(df_to)

# If all tweets have been processed
if len_before_from < 1:
        print('No more tweets!')
else:
        df_from, df_to = execute_new_post(api, df_from, df_to, FILE_FROM, FILE_TO)
        assert((len_before_from == len(df_from) + 1) and (len_before_to == len(df_to) - 1))