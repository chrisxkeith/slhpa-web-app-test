from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotSelectableException
# TODO : from django.test import TestCase
import time
import os
import platform
import sys
import datetime
import re


def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t' + script_name + '\t' + message)


def log_exception(message):
    log(message + ' : ' + str(sys.exc_info()
                              [0]) + ' : ' + str(sys.exc_info()[1]))


class Tester:
    driver = None
    wait = None

    def run_view_test(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)
        finally:
            self.driver.close()

    def run_edit_test(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)
        finally:
            self.driver.close()

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
        browser_types = ["Chrome", "Firefox"]
        if platform.system() == 'Windows':
            browser_types.append("Edge")
        if platform.system() == 'Darwin':
            browser_types.append("Safari")
        for browser_type in browser_types:
            try:
                self.set_web_driver(browser_type)
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
            except:
                log_exception('Failure in browser: ' + browser_type)

    def main(self):
        starttime = datetime.datetime.now()
        log("Started tests")
        self.run_test('https://slhpa-03.appspot.com/slhpa/', False)
        self.run_test('http://127.0.0.1:8000/slhpa/', True)
        seconds = (datetime.datetime.now() - starttime).seconds
        log("Elapsed seconds: " + str(int(seconds)))


if '__main__' == __name__:
    Tester().main()
