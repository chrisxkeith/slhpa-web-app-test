from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotSelectableException
from unittest import TestCase
import time
import os
import platform
import sys
import datetime
import re
import unittest

def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t' + script_name + '\t' + message)


def log_exception(message):
    log(message + ' : ' + str(sys.exc_info()
                              [0]) + ' : ' + str(sys.exc_info()[1]))

browsers = [ 'Firefox', 'Chrome', 'Edge', 'Safari' ]
urls = [ 'https://slhpa-03.appspot.com/slhpa/', 'https://slhpa-06.appspot.com/slhpa/', 'http://127.0.0.1:8000/slhpa/' ]

class Tester(TestCase):
    driver = None
    wait = None

    def check_row_count(self, url, c):
        time.sleep(4) # Edge :( :( :(
        rows = self.driver.find_elements(By.XPATH, "//tr")
        log("found " + str(len(rows)) + " on " + url)
        if c + 1 != len(rows):
            print('x')  # for debugging only.
        self.assertEqual(c + 1, len(rows)) # header row plus c data rows.

    def extract_count(self, index):
        search_result_count = self.driver.find_element(
            By.XPATH, "//span[contains(text(),'Search matches: ')]")
        p = re.compile(r'\d+')
        m = p.findall(search_result_count.text)
        return int(m[index])

    def verify_search(self):
        total_records = self.extract_count(1)

        search_field = self.driver.find_element_by_id('id_search_term')
        search_field.send_keys('Estudillo')

        search_button = self.driver.find_element(
            By.XPATH, "//button[contains(text(),'Search')]")
        search_button.send_keys(Keys.ENTER)
        time.sleep(3) # Firefox :( :( :(
        searched_records = self.extract_count(0)
        self.assertTrue(searched_records > 0 and searched_records < total_records)


    def verify_photo(self):
        # TODO : only checks if src attribute exists. Must be expanded to see if img file is actually there.
        images = self.driver.find_elements(By.XPATH, "//img")
        self.assertIsNotNone(images)
        for image in images:
            src = image.get_attribute("src")
            if '00000001.jpg' in src:
                return
        self.assertTrue(False, 'No img with 00000001.jpg src.')
    
    def run_base_test(self, url):
        self.driver.get(url)
        time.sleep(2)
        edit_field = self.driver.find_elements(By.XPATH, "//*[@id=\"id_resource_name__contains\"]")
        self.assertIsNot(edit_field, None)
        if 'https://slhpa-06.appspot.com/slhpa/' in url:
            self.check_row_count(url, 0)
        else:
            self.check_row_count(url, 10)
            set_to_25 = self.driver.find_element(By.XPATH, "//*[@id=\"id_records_per_page\"]/option[2]")
            set_to_25.click()
            self.check_row_count(url, 25)
            self.verify_photo()
            # If we ever want to automate search testing in old listview,
            # we must write a completely separate function.
            if not 'old/' in url:
                self.verify_search()

    def run_view_test(self, url):
        self.run_base_test(url)

    def run_edit_test(self, url):
        add_new = self.driver.find_element(
            By.XPATH, "//a[contains(text(),'Add new photo record')]")
        if add_new:
            self.assertTrue('https://slhpa-06.appspot.com/slhpa/' in url or 'http://127.0.0.1:8000/slhpa/' in url)

    def set_web_driver(self, browser_type):
        if browser_type == 'Chrome':
            self.driver = webdriver.Chrome()
        else:
            if browser_type == 'Firefox':
                self.driver = webdriver.Firefox()
            else:
                if browser_type == 'Edge':
                    self.driver = webdriver.Edge()
                else:
                    if browser_type == 'Safari':
                        self.driver = webdriver.Safari()
                    else:
                        raise "Unknown browser_type: " + browser_type

    def run_test(self, url, run_all_tests):
        time.sleep(3)
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=1,
                                    ignored_exceptions=[NoSuchElementException,
                                                        ElementNotVisibleException,
                                                        ElementNotSelectableException])
        # Implicit wait - tells web driver to poll the DOM for specified time;
        # wait is set for duration of web driver object.
        self.driver.implicitly_wait(2)

        self.run_view_test(url)
        if run_all_tests:
            self.run_edit_test(url)

    def run_local_tests(self):
        if 'http://127.0.0.1:8000/slhpa/' in urls:
            self.run_test('http://127.0.0.1:8000/slhpa/', True)

        if 'http://127.0.0.1:8000/slhpa/old/' in urls:
            self.run_test('http://127.0.0.1:8000/slhpa/old/', True)

    def run_gcp_tests(self):
        if 'https://slhpa-03.appspot.com/slhpa/' in urls:
            self.run_test('https://slhpa-03.appspot.com/slhpa/', False)

        if 'https://slhpa-03.appspot.com/slhpa/old/' in urls:
            self.run_test('https://slhpa-03.appspot.com/slhpa/old/', False)

        if 'https://slhpa-06.appspot.com/slhpa/' in urls:
            self.run_test('https://slhpa-06.appspot.com/slhpa/', True)

    def test_by_browser(self):
        for browser_type in browsers:
            if platform.system() == 'Windows' and browser_type == 'Safari':
                continue
            if platform.system() == 'Darwin' and browser_type == 'Edge':
                continue
            try:
                self.set_web_driver(browser_type)
                self.run_local_tests()
                self.run_gcp_tests()
            finally:
                self.driver.close()

if __name__ == '__main__':
    # browsers = [ "Chrome" ]
    urls = [ 'http://127.0.0.1:8000/slhpa/',
             'https://slhpa-03.appspot.com/slhpa/',
             'http://127.0.0.1:8000/slhpa/old/',
             'https://slhpa-03.appspot.com/slhpa/old/' ]
    unittest.main()
 