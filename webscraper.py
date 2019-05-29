import requests
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
        logged_in = False
        driver = webdriver.Firefox()
        home = ("https://librarysearch.temple.edu/articles?f[lang][]=eng&f[rtype][]=articles&f[tlevel][]="
                "peer_reviewed&f[tlevel][]=online_resources&f[topic][]=" + topic + "&per_page=100&q="+query)
        driver.get(home)
        window_handle = driver.current_window_handle
        print(driver.current_window_handle)
        btns_onl = driver.find_elements_by_id("online_button")
        for i in btns_onl:
            i.click()
        iframes = driver.find_elements_by_tag_name('iframe')

        cookies = driver.get_cookies()

        for i in iframes:
            ActionChains(driver).move_to_element(i)
            driver.switch_to.frame(i)
            lnks = driver.find_elements_by_tag_name('a')
            if len(lnks) < 1:
                print('something up')
            else:
                print(lnks[2].text)
                lnks[2].send_keys(Keys.RETURN)
                while len(driver.window_handles) < 2:
                    continue
            print(driver.window_handles)
            driver.switch_to.window(driver.window_handles[-1])

            if not logged_in:
                print(driver.current_window_handle)
                self.login(driver)
                logged_in = True
            driver.switch_to.window(window_handle)
            driver.switch_to.default_content()

    def login(self, driver):
        username = 'tug04599'
        password = 'Dibriczalt00'
        # inp_user = driver.find_element_by_id('username')
        # inp_pass = driver.find_element_by_id('password')
        try:
            inp_user = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            inp_pass = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
        finally:
            inp_user.send_keys(username)
            inp_pass.send_keys(password)
        driver.find_element_by_tag_name('button').click()

