from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime
from PIL import Image
import pytesseract
from random import sample
import json

class Punch:

    def __init__(self, url, account, password, punch_in_time, punch_out_time, place, do_what):
        self.url = url
        self.account = account
        self.password = password
        self.punch_in_time = punch_in_time
        self.punch_out_time = punch_out_time
        self.place = place
        self.do_what = do_what

    def Log_in(self, driver):
        driver.get(self.url)
        driver.save_screenshot('screenie.png')

        img = Image.open("screenie.png")
        cropped = img.crop((0+700, 875, 1024*2-700, 965))
        cropped.save('screenie.png')

        img = Image.open("screenie.png")
        verification = pytesseract.image_to_string(img, lang='eng')
        print(verification)
        os.remove('screenie.png')

        driver.find_element(By.CSS_SELECTOR, 'input[name="log"]').send_keys(self.account)
        driver.find_element(By.CSS_SELECTOR, 'input[name="pwd"]').send_keys(self.password)
        driver.find_element(By.CSS_SELECTOR, 'input[name="slc-captcha-answer"]').send_keys(verification)

    def Punch_in(self):

        option = webdriver.ChromeOptions()
        option.add_argument('window-size=1024x768')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        driver.set_window_size(1024, 768)

        self.Log_in(driver = driver)
        time.sleep(5)

        driver.find_element(By.XPATH, '/html/body/div/div/aside/div/ul[2]/h3').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/div/div/aside/div/ul[2]/li[1]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="sign_in1"]').click()
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="Signed"]/tbody/tr[2]/td[7]/a/i').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input[name="sign_place"]').send_keys(self.place)
        driver.find_element(By.CSS_SELECTOR, 'textarea[name="sign_daily"]').send_keys(self.do_what)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="btnSave2"]/p').click()
        time.sleep(60)

        driver.close()

    def Punch_out(self):

        option = webdriver.ChromeOptions()
        option.add_argument('window-size=1024x768')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        driver.set_window_size(1024, 768)

        self.Log_in(driver = driver)
        time.sleep(5)

        driver.find_element(By.XPATH, '/html/body/div/div/aside/div/ul[2]/h3').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/div/div/aside/div/ul[2]/li[1]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="sign_out1"]').click()
        time.sleep(60)

        driver.close()

    def Punch_time(self):
        now = datetime.now()
        week = now.weekday()
        now_without_second = str(now).split(':')[0]+':'+str(now).split(':')[1]

        if str(self.punch_in_time) in str(now_without_second) and (week != 6 and week != 5):
            return "上班"
        elif str(self.punch_out_time) in str(now_without_second) and (week != 6 and week != 5):
            return "下班"
        else:
            return "不打卡"

def main():
    while True:
        with open('Job_Description.json', encoding='utf-8') as f:
            data = json.load(f)

        where_and_do_what = sample(data['where_and_do_what'], 1)[0]

        sign = Punch(
            url = "https://oauth.thu.edu.tw/v1/wp-login.php?redirect_to=%2Fv1%2Findex.php%2Foauth%2Fauthorize%2F%3Fresponse_type%3Dcode%26client_id%3DHbr8NRBfwhwliLtJH0tTqoSjP9Lavm",
            account = data['account'],
            password = data['password'],
            punch_in_time = data['punch_in_time'],
            punch_out_time = data['punch_out_time'],
            place = where_and_do_what[0],
            do_what = where_and_do_what[1]
        )

        try:
            if sign.Punch_time() == '上班':
                sign.Punch_in()
                continue
            elif sign.Punch_time() == '下班':
                sign.Punch_out()
                continue
            else:
                print(datetime.now(), end='\r')
                continue
        except:
            continue

if __name__ == '__main__':
    main()