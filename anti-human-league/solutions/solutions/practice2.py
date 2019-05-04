from interact import Bot

BASE_URL = 'http://ahl.threatsims.com:5000/'
PRACTICE2_URL = BASE_URL + 'practice2/'

if __name__ == '__main__':
    bot = Bot()
    bot.get(PRACTICE2_URL)
    result = ''
    for i in range(100):
        result = bot.get(PRACTICE2_URL)
    print(result)
