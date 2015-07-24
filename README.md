# geolocations
A small collection of scripts for getting geo locations from twitter archives
and swarm data.

## twitter-export
This requires you to have your twitter-archive unzipped somewhere on your
machine. the script takes two parameters:

1. the path to the archive-folder containing the json files for the different
months/years. usually this is **tweetarchive/data/js/tweets/**
2. a target user name, which will be flagged separately in the output

Example run:

'python twitter-export.py /home/bastian/tweets/data/js/tweets/ gedankenstuecke'

The output contains 7 columns:
1. source
2. date
3. time
4. user
5. is this tweet a reply? yes/no (1/0)
6. is this tweet mentioning the target username? yes/no (1/0)
7. the tweet's text
8. latitude
9. longitude
10. last latitude
11. last longitude

## swarm export
This script exports your swarm checkins' latitude/longitudes along with the
name of the user that checked in with you into to a csv file, it also saves
the original JSON. It requires 3 parameters:

1. your swarm OAuth token (can be found here https://developer.foursquare.com/docs/explore)
2. the filename to which you want to save the JSON output
3. the filename to which you want to save the CSV output

Example run:

'python swarm-export.py MYKEY swarm.json swarm.csv'

The output contains 5 columns
1. source
2. date
3. time
4. user
5. latitude
6. longitude
7. with whom the checkin was
8. the last latitude
9. the last longitude
