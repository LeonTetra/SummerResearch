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
            self.driver.switch_to.window(self.driver.window_handles[-1])
            if not self.logged_in:
                self.logged_in = self.login()
            self.driver.switch_to.window(self.whandle)
            self.driver.switch_to.default_content()

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

