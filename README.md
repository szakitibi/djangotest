Introduction
============

A simple REST API based social network in [Django](https://www.djangoproject.com/), and a bot which will demonstrate functionalities of the system.

Project uses [Django](https://www.djangoproject.com/) with [mySQL](https://www.mysql.com/) database. Configure it in `config/settings.py`.

Provides REST API endpoints `users/` and `posts/` for User and Post manipulation. The user manipulation is only allowed for admin users. Post is protected by a custom permission, which allows authenticated users to read, create or like posts. The custom permission allows users to edit or delete only their own posts, and does not allow them to like their own posts.

The bot is located in `bot.py` and configurations are possible within the `bot_config.ini` file. Uses [PyHunter](https://github.com/VonStruddle/PyHunter) python wrapper for the [Hunter.io v2 API](https://hunter.io/api/docs), and signs up users with emails queried from `hunter.io`, thus **a valid API key is required** to make it work.
