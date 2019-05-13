import requests
from bs4 import BeautifulSoup

#Test Work on web scraping
def main():
    url = 'http://morse-brode.herokuapp.com/'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())


if __name__ == "__main__":
    main()
