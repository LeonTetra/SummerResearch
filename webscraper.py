import requests
from bs4 import BeautifulSoup


class WebScraper:
    # url to search site keywords are applied to the url such that the
    # webscraper will only target those results
    # results are stored in a list of JSON
    def __init__(self):
        self.results = []
        self.search()
        self.form_data = {'username': 'tug04599', 'password': '********'}

    @staticmethod
    def search(topic, query):
        search_url = 'https://librarysearch.temple.edu/articles?f[lang][]=eng&f[rtype][]=articles&f[tlevel][]=peer_reviewed&f[tlevel][]=online_resources&f[topic][]=' \
                     + topic + '&q=' + query
        response = requests.get(search_url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')