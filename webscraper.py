import requests
import os
from bs4 import BeautifulSoup
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
                "peer_reviewed&f[tlevel][]=online_resources&f[topic][]=" + topic + "&per_page=10&q="+query)
        self.whandle = None
        self.load(self.home)
        self.access = self.__get_access()
        print()

    def __get_access(self):
        access = ['', '']
        with open('access.txt', 'r') as f:
            access[0] = (f.readline()).strip('\n')
            access[1] = (f.readline()).strip('\n')
        return access

    def __identify_db(self):
        # list dbs to draw articles from. Identified by 5 character code
        # e.g. JSTOR = JSTOR and SPRNG = Springer
        dbs = ['JSTOR', 'EBSCO', 'SPRNG', 'SCIDI', 'KARGR', 'JAMAN', 'JNNPB', 'PROQS', 'WOLSK', 'JSAGE', 'OVIDS', 'ACADO', 'DUKEU', 'TANDF', 'GALEG']
        wait = WebDriverWait(self.driver, 20)
        try:
            ident = wait.until(browser_has_url_element('.libproxy'))
        except TimeoutException:
            print('UNKNOWN')
            return 'UNKNOWN'  #unknown
        print(ident)
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
        elif ident == 'o.galegroup.com' or ident == 'i.galegroup.com':
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
            if len(lnks) < 1:
                print('something up')
            else:
                lnks[2].send_keys(Keys.RETURN)
                while len(self.driver.window_handles) < 2:
                    continue
            self.driver.switch_to.window(self.driver.window_handles[1])
            if not self.logged_in:
                self.logged_in = self.login()

            self.parse()

            self.driver.switch_to.window(self.whandle)
            self.driver.switch_to.default_content()
    def parse(self):
        cur_db = self.__identify_db()
        if cur_db == 'UNKNOWN' or cur_db[0] == 'X':
            self.driver.close()


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
