import parser
import random
import time
import traceback
import yaml

from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options

from notification import notify
from exception import LimitException
from exception import TooOftenException


def load_config():
    config_file = open('config.yaml')
    return yaml.load(config_file, Loader=yaml.FullLoader)


def firefox_driver():
    ua = UserAgent()
    profile = Options()

    random_ua = ua.random
    print("User-agent:" + random_ua)
    profile.set_preference("general.useragent.override", random_ua)
    profile.add_argument("--no-sandbox")
    profile.add_argument("--ignore-certificate-errors")

    options = {
        # 'proxy': {
        #     'http': config['proxy_url'],
        # }
    }

    driver = webdriver.Firefox(options=profile,
                               seleniumwire_options=options)
    driver.set_script_timeout(3)
    driver.delete_all_cookies()
    return driver


def mine():
    cnt = 0
    try:
        config = load_config()
        app_config = config['app']
        user_config = config['user']

        driver = firefox_driver()
        # driver.minimize_window()

        url = config['termin_url']
        driver.get(url)
        prsr = parser.Parser(driver)
        prsr.start()
        print("starting...")
        while True:
            print("Counter: " + str(cnt))
            if cnt > random.randrange(app_config['min_refresh_count'], app_config['max_refresh_time']):
                print("Refresh count limit reached! Restarting")
                raise LimitException("Counter limit reached!")

            if prsr.find():
                driver.maximize_window()
                notify(title='Terminer',
                       subtitle='Termin available!',
                       message='Check the Firefox by Selenium')
                prsr.click_first_timeslot()
                prsr.fill_in_data(user_config['name'], user_config['email'], user_config['phone'])
                prsr.agree_on_terms()
                prsr.get_termin()
                time.sleep(60)
                break
            sleep_time = random.randint(app_config['min_refresh_time'], app_config['max_refresh_time'])
            print("Sleeping for " + str(sleep_time) + " seconds")
            time.sleep(sleep_time)
            cnt += 1
    except LimitException:
        print("Error happened:" + traceback.format_exc())
    except TooOftenException:
        print("Error happened:" + traceback.format_exc())
        time.sleep(60 * 30)
    except Exception:
        if driver is not None:
            driver.maximize_window()
        time.sleep(10)
        print("Error happened:" + traceback.format_exc())
        notify(title='Terminer',
               subtitle='Termin available but error happened!',
               message='Check the Firefox by Selenium')
    finally:
        driver.close()


while True:
    mine()
    print("Restarting Parser!")
