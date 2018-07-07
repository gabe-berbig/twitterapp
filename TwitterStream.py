#
import string
import time
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import UserCredentials

#Twitter authenticator
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(UserCredentials.Consumer_Key, UserCredentials.Consumer_Key_Secret)
        auth.set_access_token(UserCredentials.Access_Token, UserCredentials.Access_Token_Secret)
        return auth

#Twitter client
class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        tweets_api = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet.text)
            tweets_api.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id = self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_my_tweets(self, num_tweets):
        home_timeline_tweets = []
        self.twitter_user = 'TweetAlot5'
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet.text)
        return home_timeline_tweets

    def tweet_out_from_input(self,tweet_body):
        self.twitter_client.update_status(tweet_body)

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweet_filename, hash_tag_list):
        #this handles twitter authentication and access to the twitter streaming api
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        #This line lists the hashtags which will be tracked by the stream
        stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):
    """
    Basic listener class that prints recieved tweets to stdout
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" %str(e))
        return True

    def on_error(self,status):
        if status == 420:
            #Returning false on data method incase rate limit is flagged by twitter
            return False
        print(status)

if __name__ == "__main__":

    hash_tag_list = ["space","elonmusk","donald trump"]
    fetched_tweets_filename = "tweets.txt"

#    twitter_streamer = TwitterStreamer()
#    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

while True:
    twitter_client = TwitterClient('theMemesBot')
    temp = str(twitter_client.get_user_timeline_tweets(1))
    replaceQuotes = temp.replace('"',"",2)
    replaceLBrack = replaceQuotes.replace("[","")
    tweet_body = replaceLBrack.replace("]","")
    print(temp)
    RecentTweet = str(twitter_client.get_my_tweets(1))
    print(RecentTweet)
#    print(twitter_client.get_friend_list(3))
    if temp is not RecentTweet:
        twitter_client.tweet_out_from_input(tweet_body)
        print("Tweeted!")
    time.sleep(300)
