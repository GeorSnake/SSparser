from fake_useragent import UserAgent
from selenium import webdriver

def get_browser_options():
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.random}")
    return options