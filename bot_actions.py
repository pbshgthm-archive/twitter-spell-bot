import tweepy
from config import bot_auth
from datetime import datetime as dt
 
class Bot(tweepy.API):

	def clean_up_timeline(self):
		for tweet in tweepy.Cursor(self.user_timeline).items():
			print("Working on ",tweet.id,"  ",tweet.created_at)
			if tweet.is_quote_status:
				try:
					quoted_id=tweet.entities['urls'][0]['expanded_url']
					quoted_id=int(quoted_id.split("/")[-1])
					src=self.get_status(quoted_id)
				except:
					self.destroy_status(tweet.id)
			print("Timeline Cleaned")


	def follow_followers(self):
		self.followers_list=self.followers_ids()
		for follower in self.followers_list:
			print("Following ",follower)
			self.create_friendship(follower)
		print("Following completed")

	def unfollow_nonfollowers(self):
		self.followers_list=self.followers_ids()
		self.following_list=self.friends_ids()
		for user in self.following_list:
			print("Checking ",user)
			if user not in self.followers_list:
				print("Unfollowing ",user)
				self.destroy_friendship(user)
		print("Unfollowing completed")

	def clean_replies(self):
		inter_list=[]
		try:
			with open("inter_list.dat") as file:
						for i in file:
							inter_list.append(i)
		except:
			pass


		for tweet in tweepy.Cursor(self.user_timeline).items():

			print("Working on",tweet.id,"  ",tweet.created_at)	
			if not tweet.is_quote_status:
				try:
					resp=False
					time=tweet.created_at
					elapsed=(dt.utcnow()-time).seconds/3600
					if not elapsed>24:
						continue

					if not tweet.retweet_count==0:
						resp=True
					if not tweet.favorite_count==0:
						resp=True
					if tweet.id in inter_list:
						resp=True
					if not resp:
						self.destroy_status(tweet.id)
						print(tweet.id," destroyed")
				except Exception as e:
					print(e)					
		print("Replies Cleaned")





auth = tweepy.OAuthHandler(bot_auth['consumer_key'], bot_auth['consumer_secret'])
auth.set_access_token(bot_auth['access_token'], bot_auth['access_token_secret'])

bot=Bot(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


correct=[]
errors=[]

with open("spell.dat") as file:
	for i in file:
		errors.append(i.split("|")[0])
		correct.append(i.split("|")[1][:-1])


print('''
clean_timeline: ct
clean_replies: cr
follow_followers: ff
unfollow_nonfollowers: un
''')

opt=input("Action ?")
if opt=="ct":
	bot.clean_up_timeline()
if opt=="cr":
	bot.clean_replies()
if opt=="ff":
	bot.follow_followers()
if opt=="un":
	bot.unfollow_nonfollowers()
else:
	print("invalid")


	