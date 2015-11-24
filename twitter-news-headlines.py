#!/usr/bin/python

import twitter

auth = {'cons_key'   : 'zrXRpgDrsDCqdALY2dJFpO2QZ',
        'cons_sec'   : 'kSzSpa4FedmhXmWCNBiFGBoLB8oRGxG4jMiqwKecaKYWhphYqV',
        'access_key' : '331106524-QO1nCknIm24nTw1D9z33eyVi8LjV476jK69lOMN9',
        'access_sec' : 'dqgPna2Wr41OoWb0InpvpRdJTEKZVFAWLv7ajkSMXyaJp'}

twitter = twitter.Twitter(auth=twitter.OAuth(auth['access_key'], auth['access_sec'],
    auth['cons_key'], auth['cons_sec']))

bbc_tweets = twitter.statuses.user_timeline(screen_name = 'BBCBreaking')

last_tweet = bbc_tweets[0]['text']

print last_tweet.split('http')[0]

f = open('/home/christoph/.bbc-url', 'w')
f.write('http' + str(last_tweet.split('http')[1]))
f.close()
