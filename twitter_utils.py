import oauth2
import constants
import urllib.parse as urlparse

# create a consumer, which uses consumer_key and consumer_secret to identify our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


def get_request_token():
    client = oauth2.Client(consumer)
    # use the client to perform request for the request_token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print('An error occurred getting request token from twitter!  ')
    # Get the request token parsing the query string returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def get_oauth_verifier(request_token):
    # Ask user authorize our app and give us the pin code
    print("Go to the following site in your browser:")
    print()

    return input("What is the PIN? ")


def get_oauth_verifier_url(request_token):

    return "{}?oauth_token{}".format(constants.AUTHORIZATION_URL, request_token['oauth_token'])



def get_access_token(request_token,oauth_verifier):
    # create a token object which contains the request_token, and the verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    # create a client with our consumer(our app) and the newly created (and verifier ) token
    client = oauth2.Client(consumer, token)
    # Ask twitter for a access token, and twitter knows it should gives us it because we've verified the request token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

