import lxml
from bs4 import BeautifulSoup


# --- READING HTML FILE ---
with open('page_example.html', 'r') as  html_file:
    html_text = html_file.read()

# -- CREATING SOUP OBJECT ---
soup = BeautifulSoup(html_text, 'lxml')

# --- LOCATING ELEMENTS ON THE PAGE ---

# getting info by a tag name:
h1_headers = soup.h1

# getting text out of the tags:
print(h1_headers.string)

# finding by id:
h1_headers = soup.find('h1',id='main-heading' )
print(h1_headers.string)

# trying CSS Selector:
first_li = soup.select_one('#num-1>span')
print(first_li.text)
