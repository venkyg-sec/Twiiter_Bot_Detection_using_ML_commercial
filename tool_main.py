import twitter_bot_detect

# Enter the twitter handle
handle = raw_input("\n Enter the twitter handle \n")
output_results = twitter_bot_detect.main(handle)

print "\n", output_results

