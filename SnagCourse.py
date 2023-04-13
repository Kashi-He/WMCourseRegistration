from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
from time import sleep
import os
import smtplib


class Register(object):

    page_urls = { # urls for different pages on the site (last part of URL address)
        'home' : '/registration/registration',
        'login' : '/registration/registerPostSignIn?mode=registration',
        'select_term' : '/term/termSelection?mode=registration',
    }


    def __init__(self, username, password, term, crns):
        self.username = username
        self.password = password
        self.term = term
        self.crns = crns

        self.base_url = "https://prod.banner.wm.edu"
        self.middle_url = "/StudentRegistration/ssb"

        browser = webdriver.Firefox()

        print("Starting Login")
        self.__login__(browser)

        print("Selecting Term")
        self.__select_term__(browser)

        print("Inputting CRNs")
        self.__input_crns__(browser)
        print("CRNs Inputted")

        

    def __input_crns__(self, browser):
        WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tabbuttons > li:nth-child(2)")))
        browser.find_element(By.CSS_SELECTOR, "#tabbuttons > li:nth-child(2)").click()

        for i in range(0,len(self.crns)):
            browser.find_element(By.ID, "txt_crn1").send_keys(self.crns[0])
            browser.find_element(By.CLASS_NAME, "primary-button").click()
        browser.find_element(By.ID, "saveButton").click()
    

    def __select_term__(self, browser):
        #Wait until page is loaded
        WebDriverWait(browser, 600).until(EC.presence_of_element_located((By.CLASS_NAME, "select2-arrow")))
        sleep(1)
        browser.find_element(By.CLASS_NAME, "select2-arrow").click()
        browser.find_element(By.CLASS_NAME, "select2-result-label").click()
        browser.find_element(By.CLASS_NAME, 'form-button').click()
        print("done")


    def __login__(self, browser):
        browser.get(self.base_url + self.middle_url + self.page_urls['login'])

        #input username
        WebDriverWait(browser, 600).until(EC.presence_of_element_located((By.ID, "username")))

        browser.find_element(By.ID, "username").send_keys(self.username)

        #input password and click login
        browser.find_element(By.ID, "password").send_keys(self.password)
        browser.find_element(By.ID, "password").send_keys(Keys.ENTER)


class SearchForOpenSpot(object):
    page_urls = { 
        'search_page' : '/search?',
    }

    def __init__(self, term, SearchCRNS, targetEmail, register = False):
        self.searchCRNS = SearchCRNS
        self.base_url = "https://courselist.wm.edu/courselist/courseinfo"
        self.term = term
        self.successfulCRNS = []
        self.targetEmail = targetEmail
        self.register = register

        browser = webdriver.Firefox()
        while True:
            now = datetime.now()
            print("Time =", now.strftime("%H:%M:%S"))
            self.__search_for_open_spots__(browser)
            print("\n")
            sleep(60)

            
    def __search_for_open_spots__(self, browser):
        for i in range(0,len(self.searchCRNS)):
            #Navigate to search page
            self.__homepage__(browser)

            #Input term and subject
            self.__select_term__(browser)
            self.__select_subject__(browser, self.searchCRNS[i].split(' ', 1)[0])

            #Finding availaible spots
            browser.find_element(By.ID, "search").click()
            xpath = "//*[contains(text(),'" + self.searchCRNS[i] + "')]/../td[10]"

            #Checking if there is an open spot
            if int(browser.find_element(By.XPATH, xpath).text.replace("*", "")) > 1:
                print("\033[92m" + self.searchCRNS[i] + " is open" + "\033[0m")
                #say(self.searchCRNS[i] + " is open") 
                send_email(self.searchCRNS[i] + " is open", self.targetEmail)

                self.successfulCRNS.append(self.searchCRNS[i])
                if self.register == True:
                    Register("jhe10@wm.edu", "password", "Fall 2023", self.successfulCRNS[i])
                    send_email(self.searchCRNS[i] + " has been registered")

                
                self.searchCRNS.remove(self.searchCRNS[i])
            else:
                print(self.searchCRNS[i] + " is not open")

    def __homepage__(self, browser):
        #Gets to the homepage
        browser.get(self.base_url + self.page_urls['search_page'])
    
    def __select_term__ (self, browser):
        #Selects the term
        select = Select(browser.find_element(By.ID,'term_code'))
        select.select_by_visible_text(self.term)

    def __select_subject__ (self, browser, subject):
        #Selects the subject
        select = Select(browser.find_element(By.ID,'term_subj'))
        select.select_by_value(subject)


def say(msg = "Finish", voice = "Samantha"):
    os.system(f'say -v {voice} {msg}')

def send_email(body, targetEmail):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("developmentemail7@gmail.com", "sqyzsosyguwtgeop")
    server.sendmail("developmentemail7@gmail.com", targetEmail, body)
    server.quit()

SearchCRNS = ['GEOL 203 01', 'SOCL 304 01']

reg = SearchForOpenSpot('Fall 2023', SearchCRNS, "james.he2004@gmail.com")