# Telegram Filter Bot

Developed by 
- [**Alessandro Catalano**](https://github.com/Wornairz)
- [**Alessandro Sorbello**](https://github.com/FoxAlex98)
- [**Orazio Sciuto**](https://github.com/orazios98)

As project for the [Quality Development Course](https://github.com/UNICT-Quality-Development/) at UNICT.

## Project Goal
The goal of the project is to develop a **Telegram bot** using the Python language to filter messages from one or more Telegram channels based on specific keywords entered by the user.

## Technologies used

- [Python](https://www.python.org/)
  - [Telethon](https://docs.telethon.dev/en/stable/)
  - [Python Telegram Bot](https://python-telegram-bot.org/)
- [MongoDB](https://www.mongodb.com/)


## How to execute the project

1. Install the libraries needed first using the following command:

```bash
$ pip install -r requirements.txt
```

2. Create and populate __*.env*__ file based on the provided *.env.dist* file.<br>
   You can obtain the bot token from [@BotFather](https://t.me/BotFather) and the API HASH/ID by [creating your own Telegram App](https://my.telegram.org/auth?to=apps)

3. Run the code using the following command:
```bash
$ python main.py
```

### Software Testing

Run the following command in the main directory to obtain a report about *pytest* coverage

```bash
$ pytest --cov ./src ./tests
```
