import requests
import time
import json

from bs4 import BeautifulSoup

# ----- SETTING UP THE REQUEST -----
# it is important to have headers.
# if you dont have any headers/cookies
# the server is going to identify 
# that you are not a true user that
# searches data through a browser!
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
#   id
#   tag name
#   css selector
#   XPATH

link_list = []



# gathering links
# for pages with different bikes

# css selector: '.sidebarBlock>ul>.navList-item>a'
mtb_categories = soup.select('.sidebarBlock>ul>.navList-item>a')
for item in mtb_categories:
    link_list.append(item['href'])
    print(item['href'])

# saving pages
# for different categories
count = 0
for i, link in enumerate(link_list):
    count += 1
    print('link: ' + link + ' iteration: ' + str(i))
    
    time.sleep(1.5)
    
    response_result = requests.get(url=link, headers=headers,cookies=cookies_jar)
    with open(f'bike_pages/category_{i}.html', 'w', encoding='utf-8') as html_file:
        html_file.write(response_result.text)

# css selector for a separate
# bike on a page
# '.card-figure>a' (gets the link of the bike)

# --- SCRAPING EACH BIKE CATEGORY(page) SEPARATELY ---
my_dict = {
    'Categories':[]
}

count = 8
ID = 0
for i in range(count):
    
    
    with open(f'bike_pages/category_{i}.html', 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
    
    category = {
        'Name': soup.select_one('.page-heading').get_text(),
        'Bikes': []
    }

    # FIND the main 'tag'
    # where the main information is contained!
    bikes_containers = soup.find_all('li', class_='product') # finding by class
    
    # PARSING each bike's info
    # getting bikes' info
    for b in bikes_containers:
        bike = {
            'ID': ID,
            'link': b.findChildren('a', class_='card-figure__link')[0]['href'],
            'name': b.findChildren('a', class_='card-figure__link')[0]['aria-label'],
            'price': b.findChildren('span', class_='price price--withoutTax')[0].text
        }
        ID += 1
        category['Bikes'].append(dict(bike))

    # saving dictionary
    # with organized data
    my_dict['Categories'].append(dict(category))

# --- SAVING DATA IN JSON FORMAT ---    
with open('data.json', 'w', encoding="utf-8") as file:
        json.dump(my_dict, file, indent=4, ensure_ascii=False)
