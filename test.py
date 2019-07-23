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
        rows = self.driver.find_elements(By.XPATH, "//tr")
        log("found " + str(len(rows)) + " on " + url)
        self.assertEqual(c + 1, len(rows)) # header row plus c data rows.

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
            # TODO : Search works (count > someValue)
            # TODO : Photo exists for 00000001

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

        if 'http://127.0.0.1:8000/slhpa/new/' in urls:
            self.run_test('http://127.0.0.1:8000/slhpa/new/', True)

    def run_gcp_tests(self):
        if 'https://slhpa-03.appspot.com/slhpa/' in urls:
            self.run_test('https://slhpa-03.appspot.com/slhpa/', False)

        if 'https://slhpa-03.appspot.com/slhpa/new/' in urls:
            self.run_test('https://slhpa-03.appspot.com/slhpa/new/', False)

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
            except:
                self.fail('Failure in browser: ' + browser_type)
            finally:
                self.driver.close()

if __name__ == '__main__':
    browsers = [ "Chrome" ]
    urls = [ 'http://127.0.0.1:8000/slhpa/', 'http://127.0.0.1:8000/slhpa/new/', 
            'https://slhpa-03.appspot.com/slhpa/', 'https://slhpa-03.appspot.com/slhpa/new/' ]
    unittest.main()
 