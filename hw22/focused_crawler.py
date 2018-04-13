
import urllib
import re
import time
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()

def tag_stemmer(tag):
    token_counter = 0
    anchor_text = tag.text
    url = tag.get('href', None)
    url_tokens = str(url).split('/')
    if((anchor_text.endswith("_rain")) or (anchor_text.startswith("rain_")) or
        (anchor_text.startswith("rain-")) or (anchor_text.endswith("-rain")) or
             (anchor_text == "rain") or (anchor_text == "Rain") or
           (anchor_text.endswith("rain")) or (anchor_text.startswith("rain"))):
        token_counter = token_counter + 1

    for url_token in url_tokens:
        if ((url_token.endswith("_rain")) or (url_token.startswith("rain_")) or
                (url_token.startswith("rain-")) or (url_token.endswith("-rain")) or
                (url_token == "rain") or (url_token == "Rain") or
                (url_token.endswith("rain")) or (url_token.startswith("rain"))):
            token_counter = token_counter + 1
    if (token_counter > 0):
        return True
    else:
        return False


def filter_url(page_url):
    x = 0
    time.sleep(1)
    page_html = urllib.urlopen(page_url).read()

    soup = BeautifulSoup(page_html, "html.parser")
    soup.prettify()

    file = open("focused_crawling_html.txt", "a")
    file.write("start of file" + "\n")
    file.write(page_html)
    file.write("\n" * 10)
    file.close()

    cdiv = soup.find('div', attrs={'id': 'bodyContent'})
    a_tags = cdiv.find_all('a', attrs={'href': re.compile("^/wiki/")})


    for tag in a_tags:
        url = tag.get('href',None)
        if ("#" in str(url)):
            a_tags.remove(tag)
        elif("File:" in str(url)):
            a_tags.remove(tag)
        elif("/wiki/Main_Page" in str(url)):
            a_tags.remove(tag)
        elif (":" in str(url)):
            a_tags.remove(tag)
        else:
            if(tag_stemmer(tag)):
                f_url = "https://en.wikipedia.org" + str(tag.get('href',None))
                if f_url not in main_frontier:
                    main_frontier.append(f_url)
            main_url = "https://en.wikipedia.org" + str(url)
            if main_url not in seen:
                seen.append(main_url)
        x = x + 1
    return x



seed = "https://en.wikipedia.org/wiki/Tropical_cyclone"
main_frontier = []
seen = [seed]
number_of_url_in_depth = 1
depth = 1
count = 0
j = 0


while( j <= len(seen)):
    if ((depth > 6) or (len(main_frontier) >= 1000)):
        break

    x = filter_url(seen[j])

    if(number_of_url_in_depth != 0):
        count = count + x
        number_of_url_in_depth = number_of_url_in_depth - 1

    if (number_of_url_in_depth == 0):
        depth = depth + 1
        number_of_url_in_depth = count
        count = 0
    j = j + 1

file = open("focused_crawling_url_list.txt","w")
for url in main_frontier:
    file.write(str(url))
    file.write("\n")
file.close()