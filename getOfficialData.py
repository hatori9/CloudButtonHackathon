import io
import tweepy
import pandas as pd
from lithops import Storage


bucket='cloudbuttonhackathon'                  #Change this value if you want to change the storage bucket


def dataSearch(keysText,hashtag,number_of_tweets):                       #keys: String of the file with keys
    #Reading the keys for connection                #Hashtag: hashtag we want to search and save tweets without #
    print("Keys:\n"+keysText)
    keys= open(keysText,'r').read().splitlines()
    consumer_key=keys[0]
    consumer_secret=keys[1]
    access_token= keys[2]
    access_token_secret= keys[3]
    

    #Connecting with the cloud
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)


    #information we want to substract:
    tweets = []
    likes = []
    time = []
    retweets = []
    hashtags = []
    urls = []
    text = []
    user_mentions= []
    names = []

    #Substraction of information
    lang= " lang:en OR lang:ca"
    stringSearch="#"+hashtag + lang
    print("Searching: "+stringSearch)
    for i in tweepy.Cursor(api.search,q=stringSearch,tweet_mode="extended").items(number_of_tweets):
        tweets.append(i.full_text)
        likes.append(i.favorite_count)
        time.append(i.created_at)
        for j in i.entities["hashtags"]:
            hashtags.append(j["text"])
        #names.append(i.entities["user_mentions"][0]['screen_name'])
        urls.append(i.entities["urls"])

    #Storing Information
    storage = Storage()
    string=str(hashtags)
    storage.put_object(bucket,"hashtags.txt",string)
    


def main():
    dataSearch("keys.txt","Covid19",5)
    print("gg")

if __name__ == "__main__":
    main()