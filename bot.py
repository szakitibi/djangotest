import requests
import json
import random

# ---- config

# TODO:
#   - move it to config file
#   - read config from config file
CONFIG = dict(
    base_url='http://localhost:8000/',
    admin_credentials=dict(
        username='admin',
        password='szakitibi'
        ),
    number_of_users=0,
    max_posts_per_user=0,
    max_likes_per_user=0,
    )


# ---- helper methods

def get_session():
    """ Sets up session.

        :returns: Session object with JSON header set.
        :rtype:   requests.sessions.Session
    """

    session = requests.Session()
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        })
    return session


def login(session=None, credentials=None):
    """ Acquires JWT token and sets header on session.

        :param session: If not provided it gets default session. [optional]
        :ptype session: requests.sessions.Session

        :param credentials: User's `username` and `password`. [optional]
        :ptype credentials: dict

        :returns: Session object with header Authorization set
                  with the aquired JWT token.
        :rtype:   requests.sessions.Session
    """
    if not session:
        session = get_session()
    if not credentials:
        credentials = CONFIG['admin_credentials']
    response = session.post(CONFIG['base_url']+'api-token-auth/',
                            data=json.dumps(credentials))
    if response.status_code != 200:
        raise ValueError("Invalid credentials!")
    token = response.json()['token']
    session.headers.update({'Authorization': 'JWT %s' % token})
    return session


def logout(session):
    """ Logs out user by removing Athourization header.

        :param session: Session with JWT token set
        :ptype session: requests.sessions.Session

        :returns: Session object with header Authorization removed.
        :rtype:   requests.sessions.Session
    """

    del session.headers['Authorization']
    return session


def get_users(session):
    """ Returns users.

        :param session: Session with JWT token set.
        :ptype session: requests.sessions.Session

        :returns: Users list.
        :rtype:   requests.models.Response's json-encoded content
    """

    response = session.get(CONFIG['base_url']+'users/')
    return response.json()


# ---- bot


# cerate a user using admin
session = login()


# TODO:
#   - use emailhunter.co for users
#   - create more users based on config

user_data = dict(
    username='user1',
    password='5ecret123',
    email='user1@te.st',
    first_name='One',
    last_name='User',
    )

# session.post(CONFIG['base_url']+'users/', data=json.dumps(user_data))
session = logout(session)

# login with created user and make a post
session = login(session, credentials=dict(username=user_data['username'],
                                          password=user_data['password']))
response = session.post(
    CONFIG['base_url']+'posts/',
    data=json.dumps(dict(title='post1', text='post 1 text'))
    )
post_id = response.json().get('id')
session.headers['Authorization']

# TODO:
#   - create posts based on config
#   - do likes


# make sure user can not like it's own post
post = session.post(CONFIG['base_url']+'posts/%s/like/' % post_id).json()
assert(post.get('detail') == 'You do not have permission to perform this action.')
session = logout(session)

# do a few random likes and dislikes using admin
session = login(session)
likes = 0
dislikes = 0
for i in range(10):
    if random.getrandbits(1):
        url = 'posts/%s/like/' % post_id
        likes += 1
    else:
        url = 'posts/%s/dislike/' % post_id
        dislikes += 1
    session.post(CONFIG['base_url']+url).json()

post = session.get(CONFIG['base_url'] + 'posts/%s/' % post_id).json()
assert(post['likes'] == likes)
assert(post['dislikes'] == dislikes)
