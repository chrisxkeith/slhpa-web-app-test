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
import time
import unittest

def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t' + script_name + '\t' + message)


def log_exception(message):
    log(message + ' : ' + str(sys.exc_info()
                              [0]) + ' : ' + str(sys.exc_info()[1]))


class Tester(TestCase):
    driver = None
    wait = None

    def run_view_test(self, url):
        self.driver.get(url)
        time.sleep(2)

    def run_edit_test(self, url):
        self.driver.get(url)
        time.sleep(2)

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

    def run_test(self, url, browser_type, run_all_tests):
        if platform.system() == 'Windows' and browser_type == 'Safari':
            return
        if platform.system() == 'Darwin' and browser_type == 'Edge':
            return
        time.sleep(3)
        try:
            self.set_web_driver(browser_type)
            try:
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
            finally:
                self.driver.close()
        except:
            if browser_type == 'Chrome':
                log('No Chrome browser?')
            else:
                self.fail('Failure in browser: ' + browser_type)

    def run_one_env(self, url, editable):
        self.run_test(url, "Firefox", False)
        self.run_test(url, "Chrome", False)
        self.run_test(url, "Edge", False)
        self.run_test(url, "Safari", False)

    def test_gcp_no_edit(self):
        self.run_one_env('https://slhpa-03.appspot.com/slhpa/', False)

    def test_gcp_edit(self):
        self.run_one_env('https://slhpa-06.appspot.com/slhpa/', True)

    def test_local(self):
        self.run_one_env('http://127.0.0.1:8000/slhpa/', True)

if __name__ == '__main__':
    unittest.main()
 