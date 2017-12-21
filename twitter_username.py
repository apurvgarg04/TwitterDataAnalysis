# -*- coding: utf-8 -*-
"""
@author: apurv
"""

import json
import tweepy #https://github.com/tweepy/tweepy
import csv
import pandas as pd
import time
import numpy as np

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
l=[]
def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
     auth.set_access_token(access_key, access_secret)
     api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
     alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
     new_tweets = api.user_timeline(screen_name = screen_name,count=200) 
	
	#save most recent tweets
     alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
     oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
     while len(new_tweets) > 0:
         print "getting tweets before %s" % (oldest)
         new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
         alltweets.extend(new_tweets)	#save most recent tweets
         #update the id of the oldest tweet less one
         oldest = alltweets[-1].id - 1
         print "...%s tweets downloaded so far" % (len(alltweets))

     userd=['screen_name','description','favourites_count','followers_count','friends_count','id','location','name','listed_count','statuses_count','created_at']  
     extd=['id','retweet_count','text','retweeted','lang','favorited','in_reply_to_screen_name','in_reply_to_status_id','created_at','in_reply_to_user_id']
     lst=[]        
     for i in range(len(alltweets)):
         dct=json.loads(json.dumps(alltweets[i]._json))
         d={}
         dct1=dct['user']
         dct1 = { key:value for key,value in dct1.items() if key in userd }         
         dct1['user_id'] = dct1.pop('id')
         dct1['user_created_at'] = dct1.pop('created_at')
         dct2 = { key:value for key,value in dct.items() if key in extd }
         d = dict(dct1.items() + dct2.items())
         lst.append(d)
     return lst
 #transform the tweepy tweets into a 2D array that will populate the csv	
if __name__ == '__main__':
	#pass in the username of the account you want to download
    u1=[]
    u2=[]
    u3=[]
	#pass in the username of the account you want to download
    ulst=[u1,u2,u3]
    for j in ulst:
        for i in j:
            print i
            try:
                l=l+get_all_tweets(i)
                time.sleep(60)
            except:
                continue
        time.sleep(1000)

df=pd.DataFrame(l)
df.to_csv('outak1_raw.csv', sep=',', encoding='utf-8') #Output FIle

df1 = df.replace(np.nan,' ', regex=True)

user_nm = [x.encode('utf-8') for x in df1['screen_name'].unique().tolist()]
keywd = ['sample','test'] #keywords
wd = '|'.join(keywd)
met_lst = []
#i = user_nm[0]
#type(df2.retweeted[0])
for i in user_nm:
    df2 = df1[df1['screen_name']==i]
    df3 = df2[df2.text.str.contains(wd)]
    d_met = {}
    d_met['sreen_name'] = i
    d_met['User_name'] = [x.encode('utf-8') for x in df2.name.unique().tolist()]
    d_met['Total_tweets'] = df2.statuses_count.max()
    d_met['Tweets_scrapped'] = len(df2.index)
    d_met['Max_num_rt'] = df2.retweet_count.max()
    d_met['Max_fav_ct'] = df2.favourites_count.max()
    d_met['Follower_count'] = df2.followers_count.max()
    d_met['friends_count'] = df2.friends_count.max()
    d_met['sample_tweets'] = len(df3.index)
    d_met['Per_sample_tweets'] = len(df3.index)/df2.statuses_count.max()
    d_met['Perc_orig'] = len(df2[df2.retweeted.astype(int)==0].index)*100/df2.statuses_count.max()
    d_met['Perc_rt'] = len(df2[df2.retweeted.astype(int)==1].index)*100/df2.statuses_count.max()
    if len(df3[df3.retweeted.astype(int)==0].index)==0:
        d_met['avg rt/t_sample'] = 'inf'
    else:
        d_met['avg rt/t_sample'] = len(df3[df3.retweeted.astype(int)==1].index)*100/len(df3[df3.retweeted.astype(int)==0].index)
    met_lst.append(d_met)
df_met = pd.DataFrame(met_lst)
df.to_csv('met_oak1.csv', sep=',', encoding='utf-8')#metric File
