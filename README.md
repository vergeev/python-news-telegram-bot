# python-news-telegram-bot
The bot grabs a bunch of recent posts from [VK.com](vk.com) communities mentioning Python and some related frameworks. It then sends a random one of them in reply to ```/python_news``` command.
## Installation
Get the sources and follow the instructions in the guide:

1. ```$ git clone https://github.com/patrnk/PythonNewsTelegramBot```
2. ```$ cd PythonNewsTelegramBot```
3. ```$ pip3 install -r requierements.txt```
4. ```$ python3 installation_guide.py```

There are some things you'll need to get during the installation:
- ```VK_API_APP_ID``` (to interact with VK API)
- ```VK_ACCESS_TOKEN``` (VK won't allow to search the site without the thing)
- ```TELEGRAM_BOT_TOKEN``` (to interact with the user)

The ```installation_guide.py``` will help you with getting them.
## Usage
The general workflow goes as follows.

1. Create a list of communitites we will get news from:

  ```
  $ python3 vk_sources.py -o vk_sources.json
  ```
2. Get the posts from the communities:

  ```
  $ python3 vk_posts.py -i vk_sources.json -o posts.json
  ```
3. Launch the bot:

  ```
  $ python3 bot.py posts.json
  ```
  
## Running tests
From project directory, run
```
$ nosetests -v --with-coverage
```

## What to contribute
- Increase test coverage.
- Add news sources.

## Project Goals
- Complete the assignment for [styleru_py course](http://melevir.com/things/python_styleru/).
- Start getting used to writing tests simultaneously with writing code.
- Notice and prevent premature optimization.
- [VK API](https://vk.com/dev)
- [python-telegram-bot](https://python-telegram-bot.org/)
- [venv](https://docs.python.org/3/library/venv.html)
- GitHub Issues
- basic logging
