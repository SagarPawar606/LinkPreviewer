import requests
from bs4 import BeautifulSoup

# url = 'https://www.findcoder.io/challenges/Challenge%20To%20Build%20A%20Link%20Previewer/62e3fcc51a3d874afc22ab72'
url = 'https://www.youtube.com/watch?v=TK2i27XIzIc&ab_channel=TV9Marathi'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html5lib')

meta_data = soup.find_all('meta')
# for meta in meta_data:
#     print(meta)
# print('\n\n')

title = soup.find("meta", property="og:title")
print(title["content"])

# for meta in meta_data:
    