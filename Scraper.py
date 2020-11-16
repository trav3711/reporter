import requests, sys, os, errno, time, json, datetime
from bs4 import BeautifulSoup as bs

class Scraper(object):
    """Scrapes a news website for all available articles"""

    def __init__(self, org_name, url, tags):
        #super(Scraper, self).__init__()
        self.BASE_URL = url
        self.TAGS = tags
        self.ENDPOINTS = {}
        self.ORG_NAME = org_name


    def scrape(self):
        def set_endpoints(self):
            page = requests.get(self.BASE_URL)
            soup = bs(page.content, 'html.parser')

            nav_section_tag = self.TAGS['nav_section'][0]
            nav_section_attribute = self.TAGS['nav_section'][1]
            nav_section_attribute_name = self.TAGS['nav_section'][2]

            nav_tag = self.TAGS['navs'][0]
            nav_attribute = self.TAGS['navs'][1]
            nav_attribute_name = self.TAGS['navs'][2]

            nav_section = soup.find(nav_section_tag, attrs={nav_section_attribute: nav_section_attribute_name})
            navs = nav_section.find_all(nav_tag, href=True, attrs={nav_attribute: nav_attribute_name})
            return {n.text: n['href'] for n in navs}
            #for n in navs:
                #print(n.text + ' ' + n['href'])
                #self.ENDPOINTS[n.text] = n['href']
        self.ENDPOINTS = set_endpoints(self)

        def get_articles(self):
            """trying to get a list of all the articles"""

            for key in self.ENDPOINTS.keys():
                try:
                    topic_page = requests.get(self.ENDPOINTS[key])
                    topic_soup = bs(topic_page.content, 'html.parser')

                    articles_section = topic_soup.find(self.TAGS['articles_section'][0], attrs={self.TAGS['articles_section'][1]:self.TAGS['articles_section'][2]})
                    #print(articles_section.prettify())
                    articles = articles_section.find_all(self.TAGS['articles'][0], attrs={self.TAGS['articles'][1]:self.TAGS['articles'][2]})
                    for article in articles:
                        link = article.find('a', href=True)['href']
                        if key == 'Graphic detail':
                            link = link.replace(self.BASE_URL, '')

                        article_page = requests.get(self.BASE_URL + link)
                        #print(article_page)
                        article_soup = bs(article_page.content, 'html.parser')
                        article_title = article_soup.find(self.TAGS['title'][0], attrs={self.TAGS['title'][1]:self.TAGS['title'][2]}).text
                        article_title = article_title.replace(' ', '-').lower().replace("'", "")
                        body = article_soup.find_all(self.TAGS['body'][0], attrs={self.TAGS['body'][1]:self.TAGS['body'][2]})

                        article_date = article_soup.find(self.TAGS['date'][0], attrs={self.TAGS['date'][1]:self.TAGS['date'][2]})
                        date_replacements = ['st', 'nd', 'rd', 'th', '.', ',']
                        date_str = article_date.text
                        for str in date_replacements:
                            date_str = date_str.replace(str, '')
                        datetime_obj = datetime.datetime.strptime(date_str, '%b %d %Y')
                        article_date = datetime_obj.strftime('%m-%d-%Y')

                        full_path = 'data/{0}/{1}/{1}__{2}.txt'.format(self.ORG_NAME, article_date, article_title)

                        if not os.path.exists(os.path.dirname(full_path)):
                            try:
                                os.makedirs(os.path.dirname(full_path))
                            except OSError as exc: # Guard against race condition
                                if exc.errno != errno.EEXIST:
                                    raise

                        with open(full_path, "w") as f:
                            f.write(article_title)
                            f.write('\n')
                            f.write(article_date )
                            f.write('\n')
                            for p in body:
                                f.write(p.text)
                            print('wrote: ' + article_date + '___' + article_title)
                            f.close()
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno, article_date)
                #time.sleep(15)
        get_articles(self)



    def write_to_file():
        pass

def main():
    nyt_url = 'https://www.nytimes.com/'
    nyt_tags = {'navs':('a', 'class', ['css-1wjnrbv']),
                'nav_section':('ul', 'data-testid', 'mini-nav'),
                'articles_section':('div', 'class', 'css-13mho3u'),
                'articles':('div', 'class', 'css-1l4spti'),
                'date':('span', 'class', ['css-1sbuyqj', 'e16638kd3']),
                'title':('h1', 'data-test-id', 'headline'),
                'body':('p', 'class', ['css-158dogj', 'evys1bk0'])
                }

    economist_url = 'https://www.economist.com'
    economist_tags = {'navs': ('a', 'class', ['ds-navigation-link', 'ds-navigation-link--inverse']),
                      'nav_section': ('ul', 'class', 'ds-navigation-list-items--section'),
                      'articles_section':('div', 'class', ['layout-section-collection', 'ds-layout-grid']),
                      'articles':('div', 'class', 'teaser__text'),
                      'date':('time', 'class', 'article__dateline-datetime'),
                      'title':('span', 'class', 'article__headline'),
                      'body':('p', 'class', 'article__body-text')
                      }

    nyt = Scraper('nyt', nyt_url, nyt_tags)
    economist = Scraper('economist', economist_url, economist_tags)
    nyt.scrape()
    #print(json.dumps(nyt.ENDPOINTS, indent = 4))
    economist.scrape()
    #print(json.dumps(economist.ENDPOINTS, indent = 4))

if __name__ == '__main__':
    main()
