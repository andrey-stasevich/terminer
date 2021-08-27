import parser
import random
import time
import traceback
import yaml

from fake_useragent import UserAgent
from seleniumwire import webdriver

from notification import notify
from exception import LimitException
from exception import TooOftenException


def load_config():
    config_file = open('config.yaml')
    return yaml.load(config_file, Loader=yaml.FullLoader)


def firefox_driver():
    ua = UserAgent()
    profile = webdriver.FirefoxProfile()
    random_ua = ua.random
    print("User-agent:" + random_ua)
    profile.set_preference("general.useragent.override", random_ua)
    profile.update_preferences()

    options = {
        # 'proxy': {
        #     'http': config['proxy_url'],
        # }
    }

    driver = webdriver.Firefox(firefox_profile=profile,
                               seleniumwire_options=options)
    driver.set_script_timeout(3)
    driver.delete_all_cookies()
    return driver


def mine():
    cnt = 0
    try:
        config = load_config()

        driver = None
        driver = firefox_driver()
        driver.minimize_window()

        driver.get(config['termin_url'])
        prsr = parser.Parser(driver)
        prsr.start()
        while True:
            print("Counter: " + str(cnt))
            if cnt > random.randrange(config['min_refresh_count'], config['max_refresh_time']):
                print("Refresh count limit reached! Restarting")
                raise LimitException("Counter limit reached!")

            if prsr.find():
                driver.maximize_window()
                notify(title='Terminer',
                       subtitle='Termin available!',
                       message='Check the Firefox by Selenium')
                prsr.click_first_timeslot()
                prsr.fill_in_data(name, email, phone)
                prsr.agree_on_terms()
                prsr.get_termin()
                time.sleep(60)
                break
            time.sleep(random.randint(config['min_refresh_time'], config['max_refresh_time']))
            cnt += 1
    except LimitException:
        print("Error happened:" + traceback.format_exc())
    except TooOftenException:
        print("Error happened:" + traceback.format_exc())
        time.sleep(60 * 45)
    except Exception:
        if driver is not None:
            driver.maximize_window()
        time.sleep(90)
        print("Error happened:" + traceback.format_exc())
        notify(title='Terminer',
               subtitle='Termin available but error happened!',
               message='Check the Firefox by Selenium')
    finally:
        driver.close()


while True:
    mine()
    print("Restarting Parser!")
