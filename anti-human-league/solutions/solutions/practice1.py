from interact import Bot

BASE_URL = 'http://ahl.threatsims.com:5000/'
PRACTICE1_URL = BASE_URL + 'practice1/'

if __name__ == '__main__':
    bot = Bot()
    bot.get(PRACTICE1_URL)
    result = bot.get(PRACTICE1_URL)
    print(result)
