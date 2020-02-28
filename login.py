from user import User
from database import Database
from  twitter_utils  import consumer,get_request_token,get_oauth_verifier,get_access_token


Database.initialise(user ='postgres',password='postgre_sql',host='localhost',database='postgres')

user_email = input('Enter your e-mail')
user = User.load_from_database(user_email)
if not user:

    request_token =get_request_token()
    oauth_verifier = get_oauth_verifier(request_token)
    access_token = get_access_token(request_token,oauth_verifier)

    email = input('Enter your email: ')
    first_name = input('Enter your first name: ')
    last_name= input('Enter your last name: ')
    user = User(None,user_email,first_name,last_name,access_token['oauth_token'],access_token['oauth_token_secret'])
    user.save_to_database()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')
for tweet in tweets['statues']:
    print(tweet['text'])




