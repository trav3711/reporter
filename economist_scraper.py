import os, errno, requests, json
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://www.economist.com'
MASTER_DIC = {}

page = requests.get(BASE_URL)
soup = bs(page.content, 'html.parser')

navs = soup.find('ul', class_='ds-navigation-list-items--section')
list_items = navs.find_all('a', href=True, class_="ds-navigation-link ds-navigation-link--inverse")
for item in list_items:
    key = item.text
    MASTER_DIC[key] = {}
    MASTER_DIC[key]['link'] = item['href']

for topic in ['Leaders', 'China']:
    page = requests.get(MASTER_DIC[topic]['link'])
    soup = bs(page.content, 'html.parser')
    pages = soup.find_all('a', href=True, class_='ds-pagination__item-link')
    #print('the length: ' + str(len(pages)))
    max_page_number = 1
    if len(pages) > 1:
        max_page_number = int(pages[1].text)

    id = 0
    for i in range(1, max_page_number):
        if i != 1:
            page = requests.get(MASTER_DIC[topic]['link'] + '?page={}'.format(i))
        #print(MASTER_DIC[topic]['link'] + '?page={}'.format(i))
        soup = bs(page.content, 'html.parser')
        articles = soup.find_all('div', class_='teaser__text')
        #print(len(articles))

        for div in articles:
            try:
                #print(id)
                MASTER_DIC[topic][id] = {}
                MASTER_DIC[topic][id]['title'] = div.find('a', class_='headline-link').text
                MASTER_DIC[topic][id]['endpoint'] = div.find('a', href=True, class_='headline-link')['href']
                #sum = div.find('p', class_="teaser__description teaser__description--sc2")
                #MASTER_DIC[topic][id]['teaser'] = (div.find('p', text=True)['text']

                article_page = requests.get(BASE_URL + MASTER_DIC[topic][id]['endpoint'])
                article_soup = bs(article_page.content, 'html.parser')

                article_title = MASTER_DIC[topic][id]['title'].replace(' ', '-').lower().replace("'", "")
                article_date = article_soup.find('a', href=True, class_='article__section-edition')
                if article_date is not None:
                    article_date = article_date['href'][-10:]
                article_body = article_soup.find_all('p', class_='article__body-text')

                MASTER_DIC[topic][id]['date published'] = article_date


                path = "data/economist/{}".format(article_date)
                filename = '{}__{}.txt'.format(article_date, article_title)
                full_path = path + '/' + filename

                if not os.path.exists(os.path.dirname(full_path)):
                    try:
                        os.makedirs(os.path.dirname(full_path))
                    except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise

                with open(full_path, "w") as f:
                    f.write(article_title + ' ' + article_date)
                    f.write('\n')
                    for p in article_body:
                        f.write(p.text)
                    print('wrote: ' article_date + '___' + article_title)
                    f.close()

                id += 1
            except KeyError as k:
                pass


        json_object = json.dumps(MASTER_DIC, indent = 4)
        #print(json_object)
