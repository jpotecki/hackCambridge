#import modules
import sys
import getopt
import tweepy
import csv
import re
import json

#global variables
consumer_key = ''
consumer_secret = ''
token_key = ''
token_secret = ''
#candidate variables
candidate_name = ''
candidate_user_id = ''
start_tweet_id = ''
number_of_tweets = ''

#25073877 - trump
#693116922808963072 - trump start tweet
#20 - number of tweets

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hc:u:s:n:", ["cname=", "cuid=","startid=", "numtweets="])
    except getopt.GetoptError:
        print 'parse.py -n <candidate-name> -u <candidate-user-id> -s <start-tweet-id> -n <number-of-tweets>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'parse.py -n <candidate-name> -u <candidate-user-id> -s <start-tweet-id> -n <number-of-tweets>'
            sys.exit()
        elif opt in ("-c", "--cname"):
            candidate_name = arg
        elif opt in ("-u", "--cuid"):
            candidate_user_id = arg
        elif opt in ("-s", "--startid"):
            start_tweet_id = arg
        elif opt in ("-n", "--numtweets"):
            number_of_tweets = arg
    print 'Getting tweets with hashtags and links filtered'
    get_all_tweets(candidate_name, candidate_user_id)
    #twitterfeed(candidate_name, candidate_user_id, start_tweet_id, number_of_tweets)

def twitterfeed(candidate_name, candidate_user_id, start_tweet_id, number_of_tweets):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token_key, token_secret)
    print 'Connection made to Twitter'
    api = tweepy.API(auth)

    print 'Trying to use tweepy.Cursor'
    statuses = tweepy.Cursor(api.user_timeline, user_id=candidate_user_id, since_id=start_tweet_id).items(number_of_tweets)
    f = open(candidate_name + "_starttweetid_" + start_tweet_id + ".txt", "w") #opens a file with the candidates name
    for s in statuses:
        f.write(s.text.encode('utf8') + '\n' + '\n')
    f.close
    #data = [s.text.encode('utf8') for s in statuses]

def get_all_tweets(candidate_name, candidate_user_id):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token_key, token_secret)
    api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
    alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(user_id = candidate_user_id,count=200)

	#save most recent tweets
    alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
	    print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
	    new_tweets = api.user_timeline(user_id = candidate_user_id,count=200,max_id=oldest)

		#save most recent tweets
	    alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
	    oldest = alltweets[-1].id - 1

	    print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet.text.encode("utf-8").replace("#", ""), flags=re.MULTILINE) for tweet in alltweets]

    f = open(candidate_name + "_tweets.txt", "w") #opens a file with the candidates name
    for tweet in outtweets:
        f.write(tweet + '\n' + '\n')
    f.close

pass

def get_all_tweets_original(candidate_name, candidate_user_id):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token_key, token_secret)
    api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
    alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(user_id = candidate_user_id,count=200)

	#save most recent tweets
    alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
	    print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
	    new_tweets = api.user_timeline(user_id = candidate_user_id,count=200,max_id=oldest)

		#save most recent tweets
	    alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
	    oldest = alltweets[-1].id - 1

	    print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [tweet.text.encode("utf-8") for tweet in alltweets]

    f = open(candidate_name + "_tweets_original.txt", "w") #opens a file with the candidates name
    for tweet in outtweets:
        f.write(tweet + '\n' + '\n')
    f.close

pass

if __name__ == '__main__':
    main(sys.argv[1:])
