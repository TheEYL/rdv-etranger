#!/usr/bin/env python
from singleton_decorator import singleton
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
def my_singleton(*args):
    """

    :param cls: class to be changed as a singleton
    :return: instance of the singleton
    """
    instances = dict()

    def get_instance():
        if args[0] not in instances:
            instances[args[0]] = args[0]()
        # else: #uncomment this part in order to raise a warning related to instantiation
        #     raise UserWarning("An instantiation already exists!")
        return instances[args[0]]

    return get_instance

@my_singleton
class MyDriver:
    @staticmethod
    def get_driver():
        options = Options()
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)


@singleton
class Driver:
    @staticmethod
    def get_driver():
        options = Options()
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)