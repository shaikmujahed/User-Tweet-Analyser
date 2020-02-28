from flask import Flask,render_template,sessions,redirect,request,url_for,g
from twitter_utils import get_request_token,get_oauth_verifier_url,get_access_token
from user import User
from database import Database


app = Flask(__name__)
app.secret_key='1084'

Database.initialise(database='postgres',user='postgres',password='postgre_sql',host='localhost')

@app.before_request
def load_user():
    if 'screen_name' in sessions:
        g.user =User.load_from_database(sessions['screen_name'])

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in sessions:
        return  redirect(url_for('profile'))
    request_token = get_request_token()
    sessions['request_token'] = request_token

    return redirect(get_oauth_verifier_url(request_token))

@app.route('/logout')
def logout():
    sessions.clear()
    return redirect(url_for('homepage'))



@app.route('/auth/twitter')
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_request_token(sessions['request_token'],oauth_verifier)
    user = User.load_from_database(access_token['screen_name'])
    if not user:
        user = User(None,access_token['sreen_name'],access_token['oauth_token'],access_token['oauth_token_secret'])
        user.save_to_database()

    sessions['screen_name'] = user.screen_name
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html', user = g.user)

@app.route('/search')
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))
    tweet_texts = [{'tweet':tweet['text'],'label':'neutral'} for tweet in tweets['statuses']]
    for tweet in tweet_texts:
        r = request.post('http://text-processing.com/api/sentiment/', data = {'tweet':tweet['tweet']})
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label
    return render_template('search.html',content = tweet_texts)





app.run(port=4995,debug=True)

