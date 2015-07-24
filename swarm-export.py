# coding: utf-8
import requests
import json
import sys
import datetime

# first part taken from
# https://gist.github.com/dlo/7177249
url_template = 'https://api.foursquare.com/v2/users/self/checkins?limit=250&oauth_token={}&v=20131026&offset={}'

# If you navigate to https://developer.foursquare.com/docs/explore, Foursquare
# will generate an OAuth token for you automatically. Cut and paste that token
# below.
oauth_token = sys.argv[1]
output_file_json = sys.argv[2]
output_file_csv = sys.argv[3]
user = sys.argv[4]

# this reads the swarm checkins from their API and dumps them to
offset = 0

def fetch_foursquare(output_file_json,url_template,oauth_token,offset):
    data = []
    count = 1
    with open(output_file_json, 'w') as f:
        while True:
            # get checkins from foursquare API
            response = requests.get(url_template.format(oauth_token, offset))
            if len(response.json()['response']['checkins']['items']) == 0:
                break # no more checkins to fetch, let's stop
            data.append(response.json())
            print "### got batch " + str(count) + " from 4square"
            count += 1
            offset += 250

        f.write(json.dumps(data))
        print "## finished getting data from 4square API"

# this concludes the json part, now we iterate over the json part to get the
# csv export we will use in R later on

# yes, strictly speaking we wouldn't have to fetch this data and could use the
# array we already have, feel free to refactor!

def write_single_csv_entry(v,user,withuser,last_lat,last_long,out):
    '''
    Take venue (v), username, with & last lat/long to write to file
    '''
    dateobj = datetime.datetime.fromtimestamp(float(v['createdAt']))
    time = str(dateobj.hour) + ":" + str(dateobj.minute)
    date = str(dateobj.year) + "-" + str(dateobj.month) + "-" + str(dateobj.day)
    out.write("swarm|" + date + "|" + time + "|" + user + "|" +
        str(v["venue"]["location"]["lat"]) + "|" +
        str(v["venue"]["location"]["lng"]) + "|" +
        withuser + "|" + str(last_lat) + "|" + str(last_long) + "\n")
    last_lat = v["venue"]["location"]["lat"]
    last_long = v["venue"]["location"]["lng"]
    return (last_lat,last_long)

def foursquare_json_to_csv(input_file_json,output_file_csv,user):
    '''
    use one of the foursquare jsons created by fetch_foursquare()
    to dump a csv of it
    '''
    # read the json to variable
    z = json.load(open(input_file_json))

    # open CSV file to write to
    o = open(output_file_csv,"w")
    # this is our header. should be self-explanatory, or see README.md
    o.write("source|date|time|user|lat|long|with|last_lat|last_long\n")

    # initialize empty last coordinates
    last_lat = ""
    last_long = ""

    for batch in z: # batch consists of 250 checkins
        for v in batch["response"]["checkins"]["items"]:
            if v.has_key("venue"): # is this a venue?
                if v.has_key("with"): # did someone checkin along the user?
                    for u in v["with"]: # iterate over all of them
                        last_lat,last_long = write_single_csv_entry(v,user,
                        u["firstName"],last_lat,last_long,o)
                else:
                    last_lat,last_long = write_single_csv_entry(v,user,
                    "",last_lat,last_long,o)
    o.close()

print "## getting foursquare data from API"
fetch_foursquare(output_file_json,url_template,oauth_token,offset)
print "## dumping data to csv"
foursquare_json_to_csv(output_file_json,output_file_csv,user)
