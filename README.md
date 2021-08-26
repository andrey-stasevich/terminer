# terminer
App that mines service.berlin.de for available termins

## Description

This app opens Firefox with the defined appointment page, tries to parse calendar for available dates. If any date if available, the app tries to open first available date and click first available time. If no-one has booked this appointment, the app tries to fill in the form and click submit.
After `REFRESH_COUNT_LIMIT` the app restarts the browser - you can increase this value in main.py if you want
Forms are different and the app may stuck on any step and due to any error - someone has already booked the appointment or all timeslots has gone - just restart the application to start from the beginning.
If error happens the app waits for 90 secs to let you fix some erros on the appointment form (name, email, phone) - after this time the app will be restarted and continue to mine the site.
The app has very basic capanbilities to simulate real user usage - random delays in defined range, refresh page in `[MIN_REFRESH_TIME, MAX_REFRESH_TIME]` range.
You can minimize these settings if you have rotating proxy - you can specify `PROXY_URL` and uncomment its configuration in main.py.

## Configuration
* Update your settings in the end of `main.py` and the appointment link you want to book

## Installation
```
brew install terminal-notifier
brew install geckodriver

pip3 install pyyaml ua-parser user-agents fake-useragent
pip3 install selenium
pip3 install selenium-wire
pip3 install selenium-webdriver
```

## Run
``` 
python3 main.py
```

