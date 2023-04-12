from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep



class Register(object):

    page_urls = { # urls for different pages on the site (last part of URL address)
        'home' : '/registration/registration',
        'login' : '/registration/registerPostSignIn?mode=registration',
        'select_term' : '/term/termSelection?mode=registration',
    }


    def __init__(self, username, password, term, crns,):
        self.username = username
        self.password = password
        self.term = term
        self.crns = crns

        self.base_url = "https://prod.banner.wm.edu"
        self.middle_url = "/StudentRegistration/ssb"

        browser = webdriver.Firefox()

        print("Starting Login")
        self.__login__(browser)
        print("Login Complete")

        print("Selecting Term")
        self.__select_term__(browser)
        print("Term Selected")

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



CRNS = ['17846', '10395', '17894', '17888', '10255']
 
username = input("Enter Username: ")
password = input("Enter Passwor: ")

reg = Register(username, password, "Fall 2023", CRNS)