import requests, os, errno, time, json
from bs4 import BeautifulSoup as bs

class Scraper(object):
    """docstring for Scraper."""

    def __init__(self, url, tags):
        #super(Scraper, self).__init__()
        self.BASE_URL = url
        self.TAGS = tags
        self.ENDPOINTS = {}
        self.ARTICLES = {}

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


            #navs = soup.find_all(tag, href=True, class_=class_name)
            nav_section = soup.find(nav_section_tag, attrs={nav_section_attribute: nav_section_attribute_name})
            navs = nav_section.find_all(nav_tag, href=True, attrs={nav_attribute: nav_attribute_name})
            return {n.text: n['href'] for n in navs}
            #for n in navs:
                #print(n.text + ' ' + n['href'])
                #self.ENDPOINTS[n.text] = n['href']
        self.ENDPOINTS = set_endpoints(self)


        def get_articles():
            pass

    def write_to_file():
        pass

def main():
    nyt_url = 'https://www.nytimes.com/'
    nyt_tags = {'navs':('a', 'class', ['css-1wjnrbv']),
                'nav_section':('ul', 'data-testid', 'mini-nav'),
                }

    economist_url = 'https://www.economist.com'
    economist_tags = {'navs': ('a', 'class', ['ds-navigation-link', 'ds-navigation-link--inverse']),
                      'nav_section': ('ul', 'class', 'ds-navigation-list-items--section')
                      }

    nyt = Scraper(nyt_url, nyt_tags)
    economist = Scraper(economist_url, economist_tags)
    economist.scrape()
    print(economist.ENDPOINTS)

if __name__ == '__main__':
    main()
