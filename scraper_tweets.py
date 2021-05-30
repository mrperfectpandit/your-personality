import tweepy
from tweepy import OAuthHandler,API
import pandas as pd
import time
import os

# create Class TwitterClient
class TwitterClient(object):

    def __init__(self):

        # Access credentials
        consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' #enter consumer key
        consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #enter consumer key secret
        access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #enter access token
        access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #enter access token secret


        try:
            # OAuthHandler object 
            auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
            
            # set access token and secret 
            auth.set_access_token(access_token,access_token_secret)
            
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            
        except tweepy.TweepError as e:
            print(f"Error: Twitter Authentication Failed - \n{str(e)}") 

    def get_user_tweets(self, user):

        username = user
        count = 45

        try:
            # Create query method using parameters
            tweets = tweepy.Cursor(self.api.user_timeline,id=username,count=count).items(count)

            # Pull information from tweets iterable object
            tweets_list = [[tweet.text] for tweet in tweets]

            # Create dataframe from tweets list
            tweets_df = pd.DataFrame(tweets_list)

            return tweets_df
        
        except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(4)
    
    def get_user_followers(self,user):
        # to fetch 5 following of the user and their personality types
        username = user

        follower_ids = []
        nfollowers = 6
        print ("Getting following............................")
        users = tweepy.Cursor(self.api.friends,id = username,count=nfollowers).items(nfollowers)
        tweets_list = []
        for user in users:
            # tweet_user = []
            print ("Adding following............................")
            try:
                follower_ids.append(user.screen_name)
                tweets = tweepy.Cursor(self.api.user_timeline,id=user.screen_name).items(10)
                # print ([tweet.text for tweet in tweets])
                tweets_list.append([tweet.text for tweet in tweets])
            except tweepy.TweepError as e:
                print (e)
                time.sleep(60)
        print (tweets_list)
        tweet_df = pd.DataFrame({'follower':follower_ids})
        tweet_df["tweets"] = pd.Series(tweets_list)
        print (follower_ids)
        return tweet_df

def tweet_return(tweet_handle):
    # create object of class
    twitter = TwitterClient()
    
    tweet_path = "twitter_data/"+"tweets_"+str(tweet_handle)+".csv"
    tweet_fol_path = "twitter_data/"+"fol_"+str(tweet_handle)+".csv"
    twitter.get_user_tweets(str(tweet_handle)).to_csv(tweet_path)
    twitter.get_user_followers(str(tweet_handle)).to_csv(tweet_fol_path)

    
