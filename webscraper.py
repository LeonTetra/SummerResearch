import requests
from bs4 import BeautifulSoup


class WebScraper:
    # url to search site keywords are applied to the url such that the
    # webscraper will only target those results
    # results are stored in a list of JSON
    def __init__(self):
        self.lib_link = 'https://librarysearch.temple.edu'

    def get_search(self, topic, query):
        search_url = self.lib_link + '/articles?f[lang][]=eng&f[rtype][]=articles&f[tlevel][]=peer_reviewed&f[tlevel][]=online_resources&f[topic][]=' \
                     + topic + '&per_page=100&q=' + query
        response = requests.get(search_url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        hits = soup.find_all('h3', {'class': 'index_title document-title-heading col-sm-9 col-lg-10'})
        results = []
        for i in hits:
            num = i.text[10]
            title = i.text[21:(len(i.text)-1)]
            for j in i.children:
                if j.name == 'span' or j == '\n':
                    del j
                else:
                    link = j['href']

            results.append(Result(title, num, link))
        return results

    def get_article(self, result):
        response = requests.get(self.lib_link + result.link)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        box = soup.find('iframe')
        ifr_link = box['src']
        ifr = requests.get(ifr_link)
        soup = BeautifulSoup(ifr.content, 'html.parser')
        print(soup.prettify())
        print()


class Result:
    def __init__(self, title, num, link):
        self.title = title
        self. num = num
        self.link = link

    def __str__(self):
        return "Number: " + self.num + "| Title: " + self.title + "| Link: " + self.link
