import requests
import time

from bs4 import BeautifulSoup

# ----- SETTING UP THE REQUEST -----

url = 'https://revolutionbikeshop.com/mountain/bikes/'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}
cookies_jar = requests.get('https://www.google.com/', headers=headers).cookies

# ----- MAKING THE REQUEST -----
response_result = requests.get(url=url, headers=headers,cookies=cookies_jar)
#print(response_result.text)

# SAVING HTML
with open('bike_list_page.html', 'w', encoding='utf-8') as html_file:
    html_file.write(response_result.text)

# ----- PARSING HTML -----
# it is 2 separate steps because
# we can comment out the previous step
# and stop making unnecessary requests
# to the server. Thus, no one is going
# to block us
with open('bike_list_page.html', 'r', encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), 'lxml')

# ----- EXTRACTING DATA FROM HTML -----
# can use:
#   class
#   css selector
#   id
#   tag name
#   XPATH (the worst -> hardcoded path)

link_list = []

mtb_categories = soup.select('.sidebarBlock>ul>.navList-item>a')
for item in mtb_categories:
    link_list.append(item['href'])
    print(item['href'])

for i, link in enumerate(link_list):
    print('link: ' + link + ' ' + str(i))
    time.sleep(1.0)
    response_result = requests.get(url=url, headers=headers,cookies=cookies_jar)
    with open(f'bike_pages/cat_{i}.html', 'w', encoding='utf-8') as html_file:
        html_file.write(response_result.text)
