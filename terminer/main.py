import parser
import random
import time
import traceback

from fake_useragent import UserAgent
from seleniumwire import webdriver

from notification import notify
from limit_exception import LimitException


def firefox_driver():
    ua = UserAgent()
    profile = webdriver.FirefoxProfile()
    random_ua = ua.random
    print("User-agent:" + random_ua)
    profile.set_preference("general.useragent.override", random_ua)
    profile.update_preferences()

    options = {
        # 'proxy': {
        #     'http': 'proxy_host:proxy_port',
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
        driver = None
        driver = firefox_driver()

        driver.get(url)
        prsr = parser.Parser(driver)
        prsr.start()
        while True:
            print("Counter: " + str(cnt))
            if cnt > REFRESH_COUNT_LIMIT:
                print("Refresh count limit reached! Restarting")
                raise LimitException("Counter limit reached!")

            if prsr.find():
                notify(title='Terminer',
                       subtitle='Termin available!',
                       message='Check the Firefox by Selenium')
                prsr.click_first_timeslot()
                prsr.fill_in_data(name, email, phone)
                prsr.agree_on_terms()
                prsr.get_termin()
                time.sleep(60)
                break
            time.sleep(random.randint(60, 80))
            cnt += 1
    except LimitException:
        print("Error happened:" + traceback.format_exc())
    except Exception:
        time.sleep(90)
        print("Error happened:" + traceback.format_exc())
        notify(title='Terminer',
               subtitle='Termin available but error happened!',
               message='Check the Firefox by Selenium')
    finally:
        driver.close()


REFRESH_COUNT_LIMIT = random.randrange(15, 25)

name = "Andrey Stasevich"
email = "andrey.stasevich@gmail.com"
phone = "+4917636874685"

url = "https://service.berlin.de/dienstleistung/327537/"

while True:
    mine()
    print("Restarting Parser!")