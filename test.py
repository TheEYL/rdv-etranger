#!/usr/bin/env python
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

import smtplib
from email.mime.text import MIMEText
from datetime import datetime

GMAIL_PWD = 'colloquial'

def send_gmail(msg_file):
    with open(msg_file, mode='rb') as message:  # Open report html file for reading
        msg = MIMEText(message.read(), 'html', 'html')  # Create html message

    msg['Subject'] = ' RDV NOTIFICATION {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M"))
    msg['From'] = '47betterday@gmail.com'
    msg['To'] = 'grandeyl@gmail.com'  # NO list!

    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.ehlo()  # Extended Hello
    server.starttls()  # Put the SMTP connection in TLS (Transport Layer Security) mode.
    server.ehlo()  # All SMTP commands that follow will be encrypted.
    server.login('47betterday@gmail.com', GMAIL_PWD)
    server.send_message(msg)
    server.close()


options = Options()
# options.add_argument('--headless')
# options.add_argument('no-sandbox')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://rdv-etrangers-94.interieur.gouv.fr/')

element = driver.find_element_by_xpath('//*[@id="CPId"]')
element.send_keys('94400')

button = driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/form/div/div[6]/div/input')

button.click()

etudiant = driver.find_element_by_xpath(
    '/html/body/div[2]/div[3]/div[1]/div/div[3]/div/div/form/div/div[2]/div/div[1]/div[2]/div[1]/input')
etudiant.click();

button = driver.find_element_by_xpath('//*[@id="nextButtonId"]')
button.click()

try:
    WebDriverWait(driver, 10).until(EC.alert_is_present(),
                                    )

    alert = driver.switch_to.alert
    print(alert)
    print(alert.text)
    alert.accept()

    # send_gmail("/home/leo/PycharmProjects/rdv-etranger/Email_File.html")
    print("NO RDV FOUND AT THIS TIME")
except TimeoutException:

    send_gmail("/home/leo/PycharmProjects/rdv-etranger/Email_File.html")
    os.system('/usr/bin/spd-say "There might be a rendez-vous"')

finally:
    driver.close()