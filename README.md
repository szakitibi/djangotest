Introduction
============

A simple REST API based social network in [Django](https://www.djangoproject.com/), and a bot which will demonstrate functionalities of the system.

Project uses [Django](https://www.djangoproject.com/) with [mySQL](https://www.mysql.com/) database. Configure it in `config/settings.py`.

Provides REST API endpoints `users/` and `posts/` for User and Post manipulation. The user manipulation is only allowed for admin users. Post is protected by a custom permission, which allows authenticated users to read, create or like posts. The custom permission allows users to edit or delete only their own posts, but does not allow them to like their own posts. To like a post authenticated user has to make a POST request at `posts/<id>/like/`.

The bot is located in `bot.py` and configurations are possible within the `bot_config.ini` file. **Requires a Django superuser** to be able to sign up users. Uses [PyHunter](https://github.com/VonStruddle/PyHunter) python wrapper for the [Hunter.io v2 API](https://hunter.io/api/docs), and signs up users with emails queried from `hunter.io`, thus **a valid Hunter  API key is required**. User data is enriched with data pulled from [Clearbit](https://clearbit.com/) site with the help of [clearbit](https://pypi.org/project/clearbit/) python package, thus **a valid Clearbit  API key is required** too.