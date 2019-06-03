import requests
import os
from bs4 import BeautifulSoup
import pandas
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class WebScraper:
    # url to search site keywords are applied to the url such that the
    # webscraper will only target those results
    # results are stored in a list of JSON
    def __init__(self, topic, query):
        self.topic = topic
        self.query = query
        self.logged_in = False
        self.driver = webdriver.Firefox()
        self.home = ("https://librarysearch.temple.edu/articles?f[lang][]=eng&f[rtype][]=articles&f[tlevel][]="
                "peer_reviewed&f[tlevel][]=online_resources&f[topic][]=" + topic + "&per_page=100&q="+query)
        self.whandle = None
        self.load(self.home)
        self.access = self.__get_access()
        self.reader = DatabaseReader()
        self.data = {
            'Title': [],
            'Author': [],
            'Date Published': [],
            'Database': [],
            'Content': []
        }

    @staticmethod
    def __get_access():
        access = ['', '']
        with open('access.txt', 'r') as f:
            access[0] = (f.readline()).strip('\n')
            access[1] = (f.readline()).strip('\n')
        return access

    def __identify_db(self):
        # list dbs to draw articles from. Identified by 5 character code
        # e.g. JSTOR = JSTOR and SPRNG = Springer
        dbs = ['JSTOR', 'EBSCO', 'SPRNG', 'SCIDI', 'KARGR', 'JAMAN', 'JNNPB', 'PROQS', 'WOLSK', 'JSAGE', 'OVIDS', 'OXFAC', 'DUKEU', 'TANDF', 'GALEG']
        wait = WebDriverWait(self.driver, 20)
        try:
            ident = wait.until(browser_has_url_element('.libproxy'))
        except TimeoutException:
            # print('UNKNOWN')
            return 'UNKNOWN'  #unknown
        # print(ident)
        if ident == 'www-jstor-org':
            return dbs[0]
        elif ident == 'eb.a.ebscohost.com' or ident == 'eb.b.ebscohost.com' or ident == 'openurl-ebscohost-com':
            return dbs[1]
        elif ident == 'link-springer-com':
            return dbs[2]
        elif ident == 'www-sciencedirect-com':
            return dbs[3]
        elif ident == 'www-karger-com':
            return dbs[4]
        elif ident == 'jamanetwork-com':
            return dbs[5]
        elif ident == 'jnnp-bmj-com':
            return dbs[6]
        elif ident == 'search-proquest-com':
            return dbs[7]
        elif ident == 'login-wolterskluwer-com':
            return dbs[8]
        elif ident == 'journals-sagepub-com':
            return dbs[9]
        elif ident == 'ovidsp-tx-ovid-com':
            return dbs[10]
        elif ident == 'academic-oup-com':
            return dbs[11]
        elif ident == 'read-dukeupress-edu':
            return dbs[12]
        elif ident == 'www-tandfonline-com':
            return dbs[13]
        elif ident == 'o.galegroup.com':
            return dbs[14]
        else:
            return 'X : DATABASE OR JOURNAL NOT LISTED'

    def search(self):
        btns_onl = self.driver.find_elements_by_id("online_button")
        for i in btns_onl:
            i.click()
        iframes = self.driver.find_elements_by_tag_name('iframe')
        for i in iframes:
            self.driver.switch_to.frame(i)
            lnks = self.driver.find_elements_by_tag_name('a')
            while len(lnks) < 1:
                continue
            lnks[2].send_keys(Keys.RETURN)
            while len(self.driver.window_handles) < 2:
                continue
            self.driver.switch_to.window(self.driver.window_handles[1])
            if not self.logged_in:
                self.logged_in = self.login()

            self.parse()

            self.driver.switch_to.window(self.whandle)
            self.driver.switch_to.default_content()
        self.save_data(self.data)

    def quit(self):
        self.driver.quit()

    def save_data(self, df):
        print(self.data)

    def parse(self):
        cur_db = self.__identify_db()
        if cur_db == 'UNKNOWN' or cur_db[0] == 'X':
            print('unk')
        else:
            result = self.reader.read(self.driver, cur_db)
            if result is not None:
                self.append_to_data(result)
        self.driver.close()

    def append_to_data(self, s):
        self.data['Title'].append(s.title)
        self.data['Content'].append(s.content)
        self.data['Database'].append(s.db)
        self.data['Author'].append(s.author)
        self.data['Date Published'].append(s.date)

    def load(self, url):
        self.driver.get(url)
        self.whandle = self.driver.current_window_handle

    def login(self):
        username = self.access[0]
        password = self.access[1]
        try:
            inp_user = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            inp_pass = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
        finally:
            inp_user.send_keys(username)
            inp_pass.send_keys(password)
        self.driver.find_element_by_tag_name('button').click()
        return True


class Result:
    def __init__(self, title='', author='', db='', date='', content=''):
        self.title = title
        self.author = author
        self.db = db
        self.date = date
        self.content = content


class DatabaseReader:
    def read(self, driver, db_code):
        try:
            wait = WebDriverWait(driver, 10)
            result = self.__read(driver, wait, db_code)
            return result
        except TimeoutException:
            print('ERROR: ' + db_code + ': CANNOT LOCATE NEEDED ELEMENTS')
            return None

    def __read(self, driver, wait, db_code):
        if db_code == 'SPRNG':
            return self.__read_sprng(driver, wait)
        elif db_code == 'SCIDI':
            return self.__read_scidi(driver, wait)
        elif db_code == 'KARGR':
            return self.__read_kargr(driver, wait)
        elif db_code == 'PROQS':
            return self.__read_proqs(driver, wait)
        elif db_code == 'OXFAC':
            return self.__read_oxfac(driver, wait)
        elif db_code == 'JSAGE':
            return self.__read_jsage(driver, wait)
        elif db_code == 'TANDF':
            return self.__read_tandf(driver, wait)
        elif db_code == 'GALEG':
            return self.__read_galeg(driver, wait)
        else:
            print(db_code + ' currently not supported')
            return None

    @staticmethod
    def __read_proqs(driver, wait):
        title = wait.until(EC.presence_of_element_located((By.ID, 'documentTitle')))  #
        text = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'text')))  #
        title = wait.until(text_loaded(2, title))  #
        text = wait.until(text_loaded(5, text))  #
        info = driver.find_elements_by_class_name('titleAuthorETC')  #
        info_str = ''  #
        for i in info:  #
            info_str += i.text  #
        author = info_str[0:info_str.index('.')]  #
        date = info_str[info_str.index('(') + 1:info_str.index(')')]  #
        return Result(title=title, author=author, date=date, content=text, db='PROQS')

    @staticmethod
    def __read_oxfac(driver, wait):
            title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'wi-article-title'))).text
            text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'widget-ArticleFulltext'))).text
            date = driver.find_element_by_class_name('citation-date').text
            text = str(text).replace('\n', '').replace('\t', '  ')
            auths = driver.find_elements_by_class_name('linked-name')
            authors = []
            for a in auths:
                authors.append(a.text)
            return Result(title=title, author=authors, db="OXFAC", content=text, date=date)

    @staticmethod
    def __read_tandf(driver, wait):
        title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'NLM_article-title'))).text
        text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'article'))).text
        date = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'itemPageRangeHistory'))).text
        author = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'entryAuthor'))).text
        date = date[str(date).index(':')+2:]
        text = str(text).replace('\n', '').replace('\t', '  ')
        return Result(title=title, author=author, db="TANDF", content=text, date=date)

    @staticmethod
    def __read_galeg(driver, wait):
        title = wait.until(EC.presence_of_element_located((By.ID, 'docSummary-title'))).text
        text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'document-text'))).text
        date = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'doc-pub-details'))).text
        author = wait.until(EC.presence_of_element_located((By.ID, 'docSummary-authors'))).text
        date = date[str(date).index('(') + 1: str(date).index(')')]
        text = str(text).replace('\n', '').replace('\t', '  ')
        return Result(title=title, author=author, db="GALEG", content=text, date=date)

    @staticmethod
    def __read_jsage(driver, wait):
        title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'publicationContentTitle'))).text
        text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'article'))).text
        date = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'publicationContentEpubDate'))).text
        author = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'entryAuthor'))).text
        date = date[str(date).index('Published ') + 10:]
        text = str(text).replace('\n', '').replace('\t', '  ')
        return Result(title=title, author=author, db="JSAGE", content=text, date=date)

    @staticmethod
    def __read_sprng(driver, wait):
        title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ArticleTitle'))).text
        date = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'article-dates__first-online'))).text
        auths = driver.find_elements_by_class_name('authors__name')
        authors = []
        for a in auths:
            authors.append(a.text)
        texts = driver.find_elements_by_class_name('Para')
        text =''
        for t in texts:
            text += t.text
        return Result(title=title, author=authors, db="SPRNG", content=text, date=date)

    @staticmethod
    def __read_scidi(driver, wait):
        if '/search/' in str(driver.current_url):
            article = wait.until(EC.presence_of_element_located((By.ID, 'aa-srp-result-list-title-1')))
            article.click()
            show_dets = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'show-hide-details')))
            show_dets.click()
        title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'title-text'))).text
        date = driver.find_element_by_tag_name('p').text
        auths = driver.find_elements_by_class_name('author')
        del auths[-1]
        authors = []
        for a in auths:
            authors.append(a.text)
        text = wait.until(EC.presence_of_element_located((By.ID, 'body'))).text
        return Result(title=title, author=authors, db="SCIDI", content=text, date=date)

    @staticmethod
    def __read_kargr(driver, wait):
        title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'abstractbig'))).text
        date = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'adetails'))).text
        author = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'autoren'))).text
        text = driver.find_element_by_id('fulltext').text
        text = str(text).replace('\n', '').replace('\t', '  ')
        date = date[str(date).index('Published online: ')+len('Published Online: '):]
        date = date[:str(date).index('\n')]
        return Result(title=title, author=author, db="KARGR", content=text, date=date)

class browser_has_url_element:
    def __init__(self, expected):
        self.expected = expected

    def __call__(self, driver):
        url = str(driver.current_url)
        try:
            s: int = url.index(self.expected)
            return url[8:s]
        except ValueError:
            return False


class text_loaded:
    def __init__(self, expected, element):
        self.expected = expected
        self.element = element
    def __call__(self, driver):
        length = len(self.element.text)
        if length < self.expected:
            return False
        else:
            return self.element.text

# class element_has_css_class(object):
#     """An expectation for checking that an element has a particular css class.
#
#     locator - used to find the element
#     returns the WebElement once it has the particular css class
#     """
#
#     def __init__(self, locator, css_class):
#         self.locator = locator
#         self.css_class = css_class
#
#     def __call__(self, driver):
#         element = driver.find_element(*self.locator)  # Finding the referenced element
#         if self.css_class in element.get_attribute("class"):
#             return element
#         else:
#             return False
