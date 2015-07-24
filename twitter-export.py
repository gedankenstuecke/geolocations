# coding: utf-8
import sys
import json
import glob
from string import lower

# This is basically the setup
file_location = sys.argv[1]
target_user = sys.argv[2]
user = sys.argv[3]

def read_json(f):
    '''
    ok, this is pretty simple: open a json file, return the json-object
    '''
    fhandle = open(f).readlines()[1:] # twitter's json sucks, so ignore line 0
    fhandle = "".join(fhandle)
    json_out = json.loads(fhandle)
    return json_out

def exporter(twitter_json,target,user):
    last_lat = ""
    last_long = ""
    for tweet in twitter_json:
        text = tweet['text']
        text = text.replace("\n","").replace("|","_").replace("\r","")
        datetime = tweet['created_at']

        # check the status of the mentions
        mentions_target = "0"
        is_mention = "0"
        mentions = tweet['entities']['user_mentions']
        if mentions != []:
            is_mention = "1"
            for mention in mentions:
                if lower(mention["screen_name"]) == lower(target):
                    mentions_target = "1"
        # check whether it contains a geo location

        if tweet["geo"] != {}:
            print "twitter|" + datetime[:10] + "|" + datetime[11:16] + "|" + \
            user + "|" + is_mention + \
            "|" + mentions_target + "|" + \
            text + "|" + \
            str(tweet["geo"]["coordinates"][0]) + "|" + \
            str(tweet["geo"]["coordinates"][1]) + "|" + \
            str(last_lat) + "|" + str(last_long)
            last_lat = tweet["geo"]["coordinates"][0]
            last_long = tweet["geo"]["coordinates"][1]
        else:
            print "twitter|" + datetime[:10] + "|" + datetime[11:16] + "|" + \
            user + "|" +  is_mention + \
            "|" + mentions_target + "|" + text + "||||"

if file_location[-1] != "/":
    file_location += "/"

json_files = glob.glob(file_location+ "*.js")
print "source|date|time|user|reply|target_hit|tweet|lat|long|last_lat|last_long"
for monthly_file in json_files:
    json_object = read_json(monthly_file)
    exporter(json_object,target_user,user)
