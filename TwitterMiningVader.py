from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pandas import DataFrame
import json

consumer_key = "****"
consumer_secret = "****"

access_token = "****"
access_token_secret = "****"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

tweettext = []
positive = []
neutral = []
compound = []
negative = []
count = 0
specific_time = []
time = []
country = []
country_code = []

def reset():
    
    global count
    global tweettext
    global positive
    global neutral
    global compound
    global negative
    global country
    global country_code
    global time
    global specific_time
    
    tweettext = []
    positive = []
    neutral = []
    compound = []
    negative = []
    country =[]
    country_code = []
    count = 0
    time = []
    specific_time = []

class listener(StreamListener):
    
    def on_data(self,data):
        all_data = json.loads(data)
        
        global count
        global tweettext
        global positive
        global neutral
        global compound
        global negative
        global country
        global country_code
        global time
        global specific_time
        
        try:
            try:
                tweet = all_data['extended_tweet']['full_text']
            except:
                tweet = all_data['text']
            
            if 'RT' not in tweet:
                tweettext.append(tweet)
                interm = tweet.split(" ")
                try:
                    indices = []
                    for i, elem in enumerate(interm):
                        if 'http' in elem:
                            indices.append(i)
                        if 'https' in elem:
                            indices.append(i)
                        if '@' in elem:
                            indices.append(i)
                    for i in indices:
                        del interm[i]
                except Exception:
                    print("Http or @ not present")
                tweet = " ".join(interm)
                
                analyzer = SentimentIntensityAnalyzer()         
              
                count += 1
        
                vs = analyzer.polarity_scores(tweet)
                positive.append(vs['pos'])
                compound.append(vs['compound'])
                neutral.append(vs['neu'])
                negative.append(vs['neg'])
                
                try:
                    country.append(all_data['place']['country'])
                except:
                    country.append('N.A.')
                try:
                    country_code.append(all_data['place']['country_code'])
                except:
                    country_code.append('N.A.')
                    
                timing = all_data['created_at'].split(" ")
                
                specific_time.append(timing[3])
                
                seq = [timing[1], timing[2], timing[5]]
                timing = " ".join(seq)
                
                time.append(timing)
                
                print("Count: " + str(count))
                
                if count==100:
                    return False
                else:
                    return True
        except KeyError:
            print ("No text: " + str(KeyError))
        
    def on_error(self,status):
        print ("Error: " + str(status))

def TwitterTweets(excel_name):
    twitterStream = Stream(auth, listener(), tweet_mode= 'extended', stall_warnings=True)
    twitterStream.filter(languages=["en"], track=['Trump Kim Summit', 'SG Summit',
                         'Trump Kim', 'KimSummit','Kim Summit'])

    df = DataFrame({'Tweet (Original)':tweettext, 'Positive':positive,
                    'Negative':negative, 'Neutral':neutral, 'Compound':compound,
                    'Country':country, 'Country Code':country_code, "Date":time,
                    'Time':specific_time})
    df.to_excel(excel_name, sheet_name='sheet1', index=False)

for i in range(0, 500):
    name = "Vader_9_" + str(i) +".xlsx"
    reset()
    TwitterTweets(name)
    
