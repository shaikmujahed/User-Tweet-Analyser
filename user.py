from database import CursorFromConnectionFromPool
import oauth2
from  twitter_utils import consumer
import json



class User:
    def __init__(self,id,screen_name,oauth_token,oauth_token_secret):
        self.id = id
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    def __repr__(self):
        return "<User {}>".format(self.screen_name)

    def save_to_database(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users(screen_name,oauth_token,oauth_token_secret)VALUES(%s,%s,%s)',
                           (self.screen_name,self.oauth_token,self.oauth_token_secret))

    @classmethod
    def load_from_database(cls,screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE screen_name =%s',(screen_name,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(id=user_data[0],screen_name=user_data[1],oauth_token=user_data[2],
                           oauth_token_secret=user_data[3])
    def twitter_request(self,uri,verb):
        # create an 'AUTHORIZE_TOKEN' token object, and use that to perform API calls on behalf of user
        authorize_token = oauth2.Token(self.access_token, self.oauth_token_secret)
        authorize_client = oauth2.Client(consumer, authorize_token)

        # Make twitter API calls
        response, content = authorize_client.request(uri,verb='GET')
        if response.status != 200:
            print("An error occurred when searching!")

        return json.loads(content.decode('utf-8'))






