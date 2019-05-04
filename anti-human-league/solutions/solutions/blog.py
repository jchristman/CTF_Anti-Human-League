from interact import Bot

BASE_URL = 'http://ahl.threatsims.com:5000'
BLOG_URL = BASE_URL + '/blog/'

bot = Bot()

visited = []

def spider(soup, search_for):
    for a in soup.find_all('a', href=True):
        href = BASE_URL + a['href']
        if href in visited:
            continue
        visited.append(href)
        if not 'blog' in href:
            continue
        elif not 'page' in href:
            print('Getting next page of posts: %s' % href)
            _soup = bot.get(href)
            spider(_soup, search_for)
        else:
            # then it's a blog
            print('Searching blog for %s: %s' % (href, search_for))
            _soup = bot.get(href)
            if search_for in str(_soup):
                print('--------SEARCH TERM FOUND--------')
                print(_soup)
                print('---------------------------------')

soup = bot.get(BLOG_URL)
spider(soup, 'flag')
