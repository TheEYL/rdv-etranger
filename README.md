# RDV-Etranger

This project was developed to help me get a rdv from the French prefecture at val-de-marne. 
Their platform does not have a notification system. So, it is painful to constantly have to check manually. Moreover, the rdvs are available at random hours.
Strangely enough, when a rdv is available, in less than 5 mins all slots are booked. Almost as though some other students
have their own means to get notified. 


##Installation.

This is a python project. It was tested on linux only. So the system notification will not work on MAC OS or Windows.

The packages will have to be installed one after the other otherwise the project will fail.

    pip install selenium
    pip install <other packages in requirements.txt>


##Setup

* You need to create a token Gmail account and disable security on this account to send emails.
Instructions on this link: https://devanswers.co/allow-less-secure-apps-access-gmail-account/

* Edit the code with your `send_adr` and your `rec_adr`  with your send email address and your receive email address.

* change the absolute path of the `EMAIL_FILE.html` in main.py

##Running the code. 

Linux:

    ./main.py
