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
import sys
import datetime
import re


def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t' + script_name + '\t' + message)


class Tester:
    driver = None
    wait = None

    def run_test(self, url):
        self.driver.get(url)
        time.sleep(2)
        self.driver.close()


    def main(self):
        starttime = datetime.datetime.now()
        log("Started test")
        try:
            self.driver = webdriver.Chrome()
        except:
            self.driver = webdriver.Firefox()

        self.wait = WebDriverWait(self.driver, 10, poll_frequency=1,
                                    ignored_exceptions=[NoSuchElementException,
                                                        ElementNotVisibleException,
                                                        ElementNotSelectableException])

        # Implicit wait - tells web driver to poll the DOM for specified time;
        # wait is set for duration of web driver object.
        self.driver.implicitly_wait(2)

        # self.run_test('http://127.0.0.1/slhpa/')
        self.run_test('https://slhpa-03.appspot.com/slhpa/')
        seconds = (datetime.datetime.now() - starttime).seconds
        log("Elapsed seconds: " + str(int(seconds)))


if '__main__' == __name__:
    Tester().main()
