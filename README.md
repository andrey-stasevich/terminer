# terminer
App that mines service.berlin.de for available termins

## Description

This app opens Firefox with the defined appointment page, tries to parse calendar for available dates. If any date if available, the app tries to open first available date and click first available time. If no-one has booked this appointment, the app tries to fill in the form and click submit.
If appointment found the app tries to show the popup using `terminal-notification` to attract your attention. Also it shows this popup in case of errors - there is a chance you will be able to fix some of them.

After `REFRESH_COUNT_LIMIT` the app restarts the browser - you can increase this value in main.py if you want
Forms are different and the app may stuck on any step and due to any error - someone has already booked the appointment or all timeslots has gone - just restart the application to start from the beginning.

If error happens the app waits for 90 secs to let you fix some erros on the appointment form (name, email, phone) - after this time the app will be restarted and continue to mine the site.

The app has very basic capanbilities to simulate real user usage - random delays in defined range, refresh page in `[MIN_REFRESH_TIME, MAX_REFRESH_TIME]` range.
You can minimize these settings if you have rotating proxy - you can specify `PROXY_URL` and uncomment its configuration in main.py.

## Configuration
* Change `user` section in `config.yaml` with your details

## Installation
```
brew install firefox
brew install terminal-notifier
brew install geckodriver

pip3 install -r requirements.txt
```

## Run
``` 
python3 main.py
```

tst
