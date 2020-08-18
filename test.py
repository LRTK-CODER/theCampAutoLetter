from bs4 import BeautifulSoup
from urllib.request import urlopen

boan_news_url = urlopen('http://www.boannews.com/media/t_list.asp?mkind=0')
boan_news_soup = BeautifulSoup(boan_news_url, 'html.parser')
boan_news_index = boan_news_soup.select('#news_area > div:nth-child(1) > a:nth-child(1)')

index = boan_news_index[0]['href'][20:25]

boan_news_url = urlopen('http://www.boannews.com/media/view.asp?idx='+index)
boan_news_soup = BeautifulSoup(boan_news_url, 'html.parser')

boan_news_title = boan_news_soup.select('#news_title02')
boan_news_content = boan_news_soup.select('#news_content')


print(boan_news_title[0].text)
print(boan_news_content[0].text)