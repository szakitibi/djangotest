from pyhunter import PyHunter
import configparser
import lorem
import random
import requests
import string

ALPHANUM = string.ascii_letters+string.digits


def run():
    """ Make our bot to do its job with the help of BigHero6. """

    bot = BigHero6()

    # signup users with bot superuser
    print('Creating users.')
    bot.login()
    bot.clean_up()
    users = dict()
    for email in bot.emails:
        userdata = bot.get_userdata_for_email(email)
        response = bot.create_user(userdata)
        users[response['id']] = userdata
        print('\r'+'.'*bot.emails.index(email), end='')

    # make random posts for each user
    print('\nCreating posts.')
    for user in users.values():
        credentials = dict(username=user['username'], password=user['password'])
        bot.login(credentials)
        user['posts'] = []
        for i in range(random.randint(1, bot.max_posts_per_user)):
            post = bot.create_post()
            user['posts'].append(post['id'])
        print('\r'+'.'*i, end='')
    print('\n')

    # since no post have likes yet, get all posts
    posts_with_no_likes = bot.get_posts()

    # sort users by max number of posts
    users = sorted(users.items(), key=lambda user: len(user[1]['posts']), reverse=True)

    # do likes
    progress = 0
    while len(posts_with_no_likes) and users:
        progress += 1
        print('\rLike activity in progress ' + '.'*progress, end='')
        # login next user
        user_id, user = users.pop(0)
        credentials = dict(
            username=user['username'],
            password=user['password'],
            )
        bot.login(credentials)

        # get list of available posts randomized
        # users who have at least one post with no likes
        # current user is not allowed though
        posts = bot.get_posts()
        allowed_users = set([p['user'] for p in posts
                             if not p['likes'] and p['user'] != user_id])
        posts_allowed_to_like = [p for p in bot.get_posts()
                                 if p['user'] in allowed_users]
        random.shuffle(posts_allowed_to_like)

        # make post up to max likes per user
        for i in range(bot.max_likes_per_user):
            if not posts_allowed_to_like:
                break
            # available posts are already shuffled, just pop last
            rand_post = posts_allowed_to_like.pop()
            post_id = rand_post['id']
            bot.like_post(post_id)
            # pop it from posts with no likes list too
            if rand_post in posts_with_no_likes:
                post_index = posts_with_no_likes.index(rand_post)
                posts_with_no_likes.pop(post_index)

    print('\nLike distribution:')
    results = '\n'.join(['%d: %s' % (p['id'], '▒'*p['likes']) for p in bot.get_posts()])
    print(results)
    print('Finished!')


class BigHero6(object):
    """ A nice guy to help us get the job done. """

    def __init__(self):
        """ Read config data and create session ready to be used. """

        # read config
        config_parser = configparser.ConfigParser()
        config_parser.read('bot_config.ini')
        config = config_parser['bot']

        self.bot_credentials = dict(username=config['bot_username'],
                                    password=config['bot_password'])

        self.base_url = config['base_url']
        self.auth_token_url = self.base_url+'api-token-auth/'
        self.users_url = config['base_url']+'users/'
        self.posts_url = config['base_url']+'posts/'

        self.number_of_users = int(config['number_of_users'])
        self.max_posts_per_user = int(config['max_posts_per_user'])
        self.max_likes_per_user = int(config['max_likes_per_user'])

        # query the required number of emails from `hunter.io`
        self.hunter = PyHunter(config['email_hunter_key'])
        results = self.hunter.domain_search(
            config['domain_to_search'], limit=self.number_of_users)
        self.emails = [email['value'] for email in results['emails']]

        # create session
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            })

    def login(self, credentials=None):
        """ Acquires JWT token and sets header on session.

            :param credentials: User's `username` and `password`. [optional]
                                Defaults to bot credentials from config.
            :ptype credentials: dict
        """
        if not credentials:
            credentials = self.bot_credentials
        response = self.session.post(self.auth_token_url, json=credentials)
        if response.status_code != 200:
            raise ValueError("Invalid credentials!")
        token = response.json()['token']
        self.session.headers.update({'Authorization': 'JWT %s' % token})

    def clean_up(self):
        """ Removes all users and posts previously created. """

        users = self.get_users()
        for user in users:
            if user['is_superuser']:
                continue
            self.session.delete(self.users_url+'%s/' % user['id'])

    def create_user(self, userdata):
        """ Creates user based on input userdata.

            :params userdata: User informations.
            :ptype  userdata: dict -> keys ['username',
                                            'password',
                                            'email',
                                            'first_name',
                                            'last_name', ]

            :returns: User info.
            :rtype:   dict
        """

        response = self.session.post(self.users_url, json=userdata)
        if response.status_code != 201:
            raise ValueError("User creation failed! %s" % response.text)
        return response.json()

    def get_users(self):
        """ Returns users.

            :returns: Users list.
            :rtype:   list
        """

        response = self.session.get(self.users_url)
        return response.json()

    def create_post(self):
        """ Create a random post for currently logged in user."""

        postdata = dict(
            title=lorem.sentence(),
            text=lorem.paragraph(),
            )
        response = self.session.post(self.posts_url, json=postdata)
        if response.status_code != 201:
            raise ValueError("Post creation failed! %s" % response.text)
        return response.json()

    def get_posts(self):
        """ Returns posts.

            :returns: Posts list.
            :rtype:   list
        """

        response = self.session.get(self.posts_url)
        return response.json()

    def like_post(self, post_id):
        """ Likes input post in the name of the currently lgoged in user.

            :params post_id: A post id.
            :params ptype:   int
        """

        response = self.session.post(self.posts_url+'%d/like/' % post_id)
        if response.status_code != 200:
            raise ValueError("Post like failed! %s" % response.text)

    def get_userdata_for_email(self, email):
        """ Returns full userdata dicitonary for input email.

            :params email: An email.
            :ptype: str

            :returns: User information ready to be used for user creation.
            :rtype:   dict -> keys ['username',
                                    'password',
                                    'email',
                                    'first_name',
                                    'last_name', ]
        """

        username = email.split('@')[0]
        userdata = dict(
            username=username,
            password=''.join(random.sample(ALPHANUM, 8)),
            email=email,
            # TODO:
            #   Although hunter response has first and last name
            #   show case for enrichment will be done with clearbit.
            #   For first version generate it.
            first_name=username.split('.')[0].capitalize(),
            last_name=username.split('.')[-1].capitalize(),
            )
        return userdata

if __name__ == '__main__':
    run()
