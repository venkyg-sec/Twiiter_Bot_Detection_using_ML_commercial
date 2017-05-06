import tweepy
from tweepy.error import TweepError
import botornot
from decimal import *
import csv
import sys
import urlextractor
import os
import json
import urllib2
import time


counter = 0
#Avail customer_key, consumer_secret, access_token, access_token_secret. Create a dictionary named "cfg" having these values

cfg = { 
    "consumer_key"        : "N87ZNG8VKdOAmAH9njWsbiK8P",
    "consumer_secret"     : "pKV42F7i8gYDUPyL5zasWApJn0iJayGxtPWiTVhSv3NvpvgSPV",
    "access_token"        : "838450051395497985-vrf8BoRHYLVnNufVMhKrTSeaCziCXkX",
    "access_token_secret" : "dZ8c6dxYi6t1X0JaZJoDsiZBD0qklvETdQmBVwIzmef44" 
   }

cfg1 = { 
    "consumer_key"        : "laqkbHrYXN6r8HSipI6xNKCWP",
    "consumer_secret"     : "HLBxNVpW4v5ahLIMRqVuaPchMlKXUhZgCcIemJal0D39SjuWjI",
    "access_token"        : "797589780599083008-ZMRx3i8Ry9zrbdfkeF3D4v6iPzE3mKD",
    "access_token_secret" : "xeE3HQLhwhQB4IUksHnM86iMMIetA9RCqm8AOncJkDMjb" 
   }

cfg2 = {
    "consumer_key"        : "Pd2HJGOayvbURQHxfS329qB4u",
    "consumer_secret"     : "edJ9eNlLjWfHcvLdzertq01LllqNM1CQ8C1Kz2bKUqUzNpLPrz",
    "access_token"        : "777705173145837568-k4GP1m6StklfyQhr1lpeShGfLY2su7d",
    "access_token_secret" : "HBx2B2KkK5TxHXizAAYNIHOQ67YjjDZ0U0x51GwEn8tCl"
   }


def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth, wait_on_rate_limit = True)

	
	

def check_for_bots(check_list):
  
  length = len(check_list)
  counter = 0 # Maintain a counter for number of successive tweets having a time difference less than 10 seconds

  for i in range(0,length -1):

     difference = check_list[(length -1) - (i+1)][1] - check_list[(length -1) - i][1]
    
     #print "Seconds:", difference.total_seconds()
     
     if (int(difference.total_seconds()) < 5):
         counter+=1
  return counter

def get_place(tweet):
	#print type(tweet.place)

	if isinstance(tweet.place, type(None)):
		#print "Location not traceable"
		x = 2	
	else:
		print "This tweet is from: ", tweet.place.country, "and city ", tweet.place.full_name , " and is in language: ", tweet.lang
		print "Co-ordinates ", tweet.place.bounding_box.coordinates
		

def get_all_tweets(screen_name):
  auth = tweepy.OAuthHandler("laqkbHrYXN6r8HSipI6xNKCWP", "HLBxNVpW4v5ahLIMRqVuaPchMlKXUhZgCcIemJal0D39SjuWjI")
  auth.set_access_token("797589780599083008-ZMRx3i8Ry9zrbdfkeF3D4v6iPzE3mKD","xeE3HQLhwhQB4IUksHnM86iMMIetA9RCqm8AOncJkDMjb")
  api = tweepy.API(auth)
  alltweets = []
  check_list = []
  check_tup = []
  new_tweets = api.user_timeline(screen_name = screen_name,count=200)
  alltweets.extend(new_tweets)
  oldest = alltweets[-1].id - 1
  while len(new_tweets) > 0:
     print "getting tweets before %s" % (oldest)
     new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
     alltweets.extend(new_tweets)
     oldest = alltweets[-1].id - 1
     print "...%s tweets downloaded so far" % (len(alltweets))
  outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
  texts_from_all_tweets = ""
  #print type(tweet.created_at)
  for t in alltweets: # Make a tuple & thereby a list of the attributes of a tweet
        #print screen_name, "'s tweet with ID ", t.id_str,  " has been retweeted ", t.retweet_count , " times"
	get_place(t)
	check_tup = [t.id_str,t.created_at,t.text.encode("utf-8")]
	check_list.append(check_tup)
	text = t.text.encode("utf-8")
	texts_from_all_tweets = texts_from_all_tweets + " " + text 
	

	 
  
  # Checking for url's from the text part of all tweets
  #check_for_urls(texts_from_all_tweets)
	
  with open('%s_tweets.csv' % screen_name, 'wb') as f:
     writer = csv.writer(f)
     writer.writerow(["id","created_at","text"])
     writer.writerows(outtweets)
  pass

  check = check_for_bots(check_list) # Send the list we created to a function check_for_bots which checks for the time difference between successive tweets
  print "Number of successive tweets with a time difference less than 1 second:", check
  if check >= 5:
	#print screen_name, " is a bot" # We report that the current entity is a bot if check is greater than 40
	return True , check
  else:
	#print screen_name, " is a human"
	return False , check
	
def check_for_urls(text_complete):
	avail = urlextractor.parseText(text_complete)
	#print avail
	#print len(avail)
	array = []
	if len(avail) > 0:
		for i in range(0,len(avail)):
			array.append(avail[i][1])
	

		for i in array:
		    data=json.dumps({
			"client": {
			  "clientId":      "Johns_Hopkins_Student",
			  "clientVersion": "1.5.2"
			},
			"threatInfo": {
			  "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING","POTENTIALLY_HARMFUL_APPLICATION","THREAT_TYPE_UNSPECIFIED"],
			  "platformTypes":    ["WINDOWS","LINUX","IOS","OSX","CHROME","ANDROID","ANY_PLATFORM"],
			  "threatEntryTypes": ["URL"],
			  "threatEntries": [
			    {"url": i}
			  ]
			}
		      }
		    )
		    #print type(data)
		    request=urllib2.Request("https://safebrowsing.googleapis.com/v4/threatMatches:find?key=AIzaSyCs4mdWV_5Iu5u3_FMnCu06yPs5Dyw81rQ",data,headers={'content-type':'application/json'})
		    response=urllib2.urlopen(request)
		    page=response.read()
		    l= json.loads(page)
		    if len(l)!=0:
	    		    print "Response:"+page
	
	


def get_skew_rate(current_user,b):
	lenb = len(b)
	if lenb is  0:
			lenb = 1
	
	if lenb < current_user.followers_count: 
	
		skew_rate = current_user.followers_count/lenb
	else :
		skew_rate = Decimal(current_user.followers_count)/Decimal(lenb)
	return skew_rate	
	
def climax(new_user,bon,api):
	  handle = "@" + new_user.screen_name
	  result = bon.check_account(handle)
	  maintain_results =[]
	  global counter
	  
          
	  if result > 0.48:
		botornot_decision = True
	  else:
		botornot_decision = False

	  print new_user.screen_name + " = " + str(result["score"])
	  print "###############################"
	  for key in result["categories"]:

			print key, " = ", result["categories"][key]

	  print "###############################"		
	  print "Printing all tweets now"
	  time_decision, value = get_all_tweets(new_user.screen_name)
	  return_list = api.friends_ids(screen_name=new_user.screen_name)
	  
	  print "The number of followers for", new_user.screen_name, " are ",  new_user.followers_count, " and he is following ", len(return_list)
	  skew= get_skew_rate(new_user,return_list)
	  if skew <= 0.05:
	  	skew_decision = True
	  else:
	  	skew_decision = False

	  print "The skew rate is: ", skew

	  
	  print new_user.screen_name, " has ", new_user.status.retweet_count, " retweets"
	  
	  if ( (skew_decision and time_decision) or (botornot_decision and time_decision) or (skew_decision and botornot_decision)):
	  	print new_user.screen_name, " is a bot"
	
	  else:
		print new_user.screen_name, "is NOT a BOT"

	  dec = ""
	  if result["score"] > 0.48:
		dec = "Yes"
	  else:
		dec = "No"
	  tup1 = (value, skew, new_user.status.retweet_count, result["score"],dec)
	  return tup1
	  

def main():
  api = get_api(cfg) #this is for initializing the Tweepy API.
  bon = botornot.BotOrNot(**cfg) #this is for the botornot API.
  
  stringofhope = "" 	
  print " Welcome to the Twitter Bot Detection Arena \n "
  print	"We present the below modes of operation \n 1)Mode-1: Monitor the current configured user's friend \n 2)Mode-2: Monitor the current user's account itself \n 3) Mode-3 : Monitor any user's account by providing their Twitter Handle \n 4) Mode-4 :Monitor the friends and followers of any user's account by providing their twitter handle \n "
  mode = raw_input("Enter the mode of operation (1,2,3 or 4)\n")
# below case to monitor current user's friends 

  if mode == "1":
	  for friend in tweepy.Cursor(api.friends).items(): #fetching friend's list from Twitter.
		climax(friend,bon,api)

# below case to monitor current user        
  elif mode == "2":

	  current_user = api.me()
	  print "The number of followers for", current_user.screen_name, " are ",  current_user.followers_count
	  
	  return_list = api.friends_ids(screen_name=current_user.screen_name)
	  print "I am following:" , len(return_list)
	  climax(current_user,bon,api)

# below case to monitor a particular user
  elif mode== "3":
	
	  try:
		  user = api.me()

		  account_name = raw_input(" Enter the user's twitter handle without @ \n")
		  new_user = api.get_user(screen_name=account_name)
	          f_list =[]
	 	  maintain_results = climax(new_user,bon,api)
		  f_list.append(maintain_results)
		  with open("%s_climax_results_mode3.csv" %new_user.screen_name , 'wb') as f:
	  	  	writer = csv.writer(f)
	 	  	writer.writerow([" Time Difference Value", " Skew Rate", "Number of retweets","Bot or Not Score", "Decision"])
		  	writer.writerows(f_list)
	  
                  pass
	  
	  
	  except TweepError:
	  	print TweepError.message[0]['code']


# below case to monitor a particular user's followers
  elif mode=="4":
	while(True):
		try :		
		  	user = api.me()
			account_name = raw_input(" Enter the user's twitter handle without @ \n")
			new_user = api.get_user(account_name)
			return_list = api.friends_ids(screen_name = new_user.screen_name)
			final_list = []
			for friends in range(0,len(return_list)):
	
				  friend_user = api.get_user(return_list[friends])
				  
				  print " Analysing User : ", 
				  tup1 = climax(friend_user,bon,api)
				  final_list.append(tup1)
				  
				  


			with open("%s_climax_result_automate.csv" %new_user.screen_name , 'wb') as f:
				writer = csv.writer(f)
			 	writer.writerow([" Time Difference Value", " Skew Rate", "Number of retweets","Bot or Not Score","Decision"])
				writer.writerows(final_list)
			pass	
	
		except tweepy.TweepError:
			time.sleep(60 * 15)
			continue
		except StopIteration:
			break	

  else:
	print " Invalid input, Perform the operations again"
		
	
  
if __name__ == "__main__":
  main()
