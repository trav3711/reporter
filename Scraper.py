import requests, sys, os, errno, time, json, datetime
from bs4 import BeautifulSoup as bs

class News_Scraper(object):
    """Scrapes a news website for all available articles"""

    def __init__(self, org_name):
        #super(Scraper, self).__init__()

        orgs = {
            'nyt':{
                'url':'https://www.nytimes.com/',
                'tags':{'navs':('a', 'class', ['css-1wjnrbv']),
                        'nav_section':('ul', 'data-testid', 'mini-nav'),
                        'articles_section':('div', 'class', 'css-13mho3u'),
                        'articles':('div', 'class', 'css-1cp3ece'),
                        'date':('span', 'data-testid', 'todays-date'),
                        'title':('h1', 'data-test-id', 'headline'),
                        'body':('p', 'class', ['css-158dogj', 'evys1bk0'])
                        }
                },
            'economist':{
                'url':'https://www.economist.com',
                'tags':{'navs': ('a', 'class', ['ds-navigation-link', 'ds-navigation-link--inverse']),
                        'nav_section': ('ul', 'class', 'ds-navigation-list-items--section'),
                        'articles_section':('div', 'class', ['layout-section-collection', 'ds-layout-grid']),
                        'articles':('div', 'class', 'teaser__text'),
                        'date':('time', 'class', 'article__dateline-datetime'),
                        'title':('span', 'class', 'article__headline'),
                        'body':('p', 'class', 'article__body-text')
                        }
                }
        }

        try:
            self.BASE_URL = orgs[org_name]['url']
            self.TAGS = orgs[org_name]['tags']
            #print(self.TAGS)
            self.ENDPOINTS = {}
            self.ORG_NAME = org_name
        except:
            print("Sorry that's not a valid news organization")


    def scrape(self):
        json_payload = {}
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

        self.ENDPOINTS = set_endpoints(self)

        def get_articles(self):
            """trying to get a list of all the articles"""

            for key in self.ENDPOINTS.keys():
                print(key)
                json_payload[key] = {}

                try:
                    print(self.ENDPOINTS[key])
                    topic_page = requests.get(self.ENDPOINTS[key])
                    topic_soup = bs(topic_page.content, 'html.parser')

                    articles_section = topic_soup.find(self.TAGS['articles_section'][0], attrs={self.TAGS['articles_section'][1]:self.TAGS['articles_section'][2]})
                    articles = articles_section.find_all(self.TAGS['articles'][0], attrs={self.TAGS['articles'][1]:self.TAGS['articles'][2]})

                    id = 0
                    for article in articles:

                        link = article.find('a', href=True)['href']
                        if key == 'Graphic detail':
                            link = link.replace(self.BASE_URL, '')

                        #get raw article page
                        article_page = requests.get(self.BASE_URL + link)
                        article_soup = bs(article_page.content, 'html.parser')

                        #format article title
                        article_title = article_soup.find(self.TAGS['title'][0], attrs={self.TAGS['title'][1]:self.TAGS['title'][2]}).text
                        article_title = article_title.replace(' ', '-').lower().replace("'", "")
                        body = article_soup.find_all(self.TAGS['body'][0], attrs={self.TAGS['body'][1]:self.TAGS['body'][2]})

                        #format date
                        article_date = article_soup.find(self.TAGS['date'][0], attrs={self.TAGS['date'][1]:self.TAGS['date'][2]})
                        #print(article_date)
                        date_replacements = ['st', 'nd', 'rd', 'th', '.', ',']
                        date_str = article_date.text
                        for str in date_replacements:
                            date_str = date_str.replace(str, '')
                        datetime_obj = datetime.datetime.strptime(date_str, '%b %d %Y')
                        article_date = datetime_obj.strftime('%m-%d-%Y')
                        #print(article_date)

                        #handle article body text
                        paragraphs = []
                        for p in body:
                            paragraphs.append(p.text)

                        json_payload[key][id] = {
                            'title':article_title,
                            'date_published':article_date
                            #'body_text': ' '.join(paragraphs)
                        }
                        id += 1
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                #time.sleep(15)
            #print(json_payload)
            return json_payload
        return get_articles(self)

#The below main is for testing purposes
def main():
    nyt = News_Scraper('nyt')
    economist = News_Scraper('economist')
    nyt.scrape()
    economist.scrape()

if __name__ == '__main__':
    main()
