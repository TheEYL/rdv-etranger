#!/usr/bin/env python
import os
import smtplib
import time
from datetime import datetime
from datetime import time as time2
from email.mime.text import MIMEText

import schedule
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

"""@Author: Yvon Leonce Eyog"""

GMAIL_PWD = 'XXXXXXXXXXXXXXX' #Insert gmail password here
SEND_ADR= 'send@gmail.com' #insert gmail sender
REC_ADR = 'receive@gmail.com'  # comma separated receiving email addresses

def send_gmail(msg_file):
    with open(msg_file, mode='rb') as message:  # Open report html file for reading
        msg = MIMEText(message.read(), 'html', 'html')  # Create html message

    msg['Subject'] = ' RDV NOTIFICATION {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M"))
    msg['From'] = SEND_ADR
    msg['To'] = REC_ADR

    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.ehlo()  # Extended Hello
    server.starttls()  # Put the SMTP connection in TLS (Transport Layer Security) mode.
    server.ehlo()  # All SMTP commands that follow will be encrypted.
    server.login(SEND_ADR, GMAIL_PWD)
    server.send_message(msg)
    server.close()


def notifyMe(driverobj):
    link = 'RDV available'
    cla = None
    try:
        cla = driverobj.find_element_by_xpath(

            '/html/body/div[2]/div[3]/div[1]/div/div[3]/div[1]/form/div[3]/fieldset/div/div[3]/div[3]')
        if cla.is_enabled():
            os.system('notify-send ' + link)
            # send_gmail("/home/leo/PycharmProjects/rdv-etranger/Email_File.html")
            send_gmail("/home/leo/PycharmProjects/rdv-etranger/Email_File.html")  #give absolute path of your file
            os.system('/usr/bin/spd-say "There might be a rendez-vous"')

    except Exception as e:
        # print("Notify failed")
        pass


def setup(driverobj):
    # options.add_argument('--headless')
    # options.add_argument('no-sandbox')
    load_page(driverobj)

    element = driverobj.find_element_by_xpath('//*[@id="CPId"]')
    element.send_keys('94400')

    button = driverobj.find_element_by_xpath('/html/body/div/div[4]/div[1]/form/div/div[6]/div/input')

    button.click()

    etudiant = driverobj.find_element_by_xpath(
        '/html/body/div[2]/div[3]/div[1]/div/div[3]/div/div/form/div/div[2]/div/div[1]/div[2]/div[1]/input')
    etudiant.click()

    button = driverobj.find_element_by_xpath('//*[@id="nextButtonId"]')
    button.click()


def load_page(driverobj):
    driverobj.get('https://rdv-etrangers-94.interieur.gouv.fr/')


def querySite(driverobj):
    try:
        setup(driverobj)
    except Exception as e:
        print("Setup error:" + e)
    try:
        WebDriverWait(driverobj, 5).until(EC.alert_is_present(),
                                          )

        alert = driverobj.switch_to.alert

        nordv = alert.text
        print(nordv)
        alert.accept()
        if 'pas' in nordv:
            # driver.get('https://rdv-etrangers-94.interieur.gouv.fr/')
            pass
            # driver.close()
            load_page(driverobj)
        else:
            try:
                notifyMe(driverobj)
                # time.sleep(500000)
            except Exception as e:
                # print("QuerySite: " + str(e))
                # driver.get('https://rdv-etrangers-94.interieur.gouv.fr/')
                load_page(driverobj)
                pass
                # driver.close()
    except TimeoutException:
        notifyMe(driverobj)
        time.sleep(3600)


def select_date_time(driverobj):
    """TO-DO: get the calendar object. Select the  latest day. Select the time dropbox. Get the latest hour. Click continue"""

    calendar = driverobj.find_element_by_xpath()  # getxpath
    hour = driverobj.find_element_by_xpath()  # getxpath
    calendar.get

    button = driverobj.find_element_by_xpath('//*[@id="nextButtonId"]')
    button.click()
def init_browser():
    from driver import Driver
    driver = Driver().get_driver()
    return driver


# def is_time_between(begin_time, end_time, check_time=None):
#     # If check time is not given, default to current UTC time
#     check_time = check_time or datetime.utcnow().time()
#     if begin_time < end_time:
#         return check_time >= begin_time and check_time <= end_time
#

driver = init_browser()


def cron():
    week = datetime.today().weekday()
    now = datetime.now()
    now_time = now.time()
    # if is_time_between(time2(8, 00), time2(18, 20)) and week < 5:
    if now_time >= time2(8, 00) and now_time <= time2(18, 30):
        if week < 5:
            print('Starting browser... ' + str(now_time))
            querySite(driver)
        else:
            print("Wrong weekday")
            # time.sleep(172800)
    else:
        print('Currently sleeping: ' + str(now_time))
        time.sleep(3600)


schedule.every(19).seconds.do(cron)

while True:
    schedule.run_pending()
    time.sleep(1)
