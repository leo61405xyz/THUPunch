from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime,timezone,timedelta
from PIL import Image
import pytesseract
from random import sample
import json
import sys, cv2
import numpy as np
import re
import shutil
from glob import glob

def slice_img(img, path):
    if not os.path.exists(path):
        os.makedirs(path)

    img_src = cv2.imread(img)
    img_b, img_g, img_r = cv2.split(img_src)

    #cv2.imwrite('img_r.jpg', img_r)

    img_gray = cv2.bitwise_not(img_r)
    img_gray = cv2.medianBlur(img_gray, 5)
    thresh_bin, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)

    #cv2.imwrite('img_bin.jpg', img_bin)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 25))
    img_eroded = cv2.erode(img_bin, kernel)

    res = cv2.findContours(img_eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = res[0]

    for i in range(0, len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        #print(i, len(contours[i]))
        #if len(contours[i]) < 10:continue
        cv2.rectangle(img_src, (x, y), (x + w, y + h), (255, 0, 0), 10)
        new_img = img_src[y:y + h, x:x + w]
        cv2.imwrite(os.path.join(path,  str(i)+'.jpg'), new_img)

    #cv2.imwrite('img_dilated_with_contours.jpg', img_src)

def remove_non_arabic_numerals(text):
    return re.sub(r'\D+', '', text)

def get_verification_code(path):

    potential_verification = []
    for f in glob('./{0}/*.jpg'.format(path)):
        img = Image.open(f)
        verification = pytesseract.image_to_string(img, lang='eng')
        verification = remove_non_arabic_numerals(text = verification)
        if len(verification) == 3 and verification.isnumeric():
            potential_verification.append(verification)

    return potential_verification[0] if potential_verification else None

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

        slice_img('screenie.png', path='out')
        verification = get_verification_code(path='out')

        print('Verification: {0}'.format(verification))
        os.remove('screenie.png')
        shutil.rmtree('out')

        driver.find_element(By.CSS_SELECTOR, 'input[name="log"]').send_keys(self.account)
        driver.find_element(By.CSS_SELECTOR, 'input[name="pwd"]').send_keys(self.password)
        driver.find_element(By.CSS_SELECTOR, 'input[name="slc-captcha-answer"]').send_keys(verification)
        driver.find_element(By.XPATH, '//*[@id="wp-submit"]').click()

    def Punch_in(self, driver):

        self.Log_in(driver = driver)
        time.sleep(5)

        driver.find_element(By.XPATH, '/html/body/div/header/div/div/a[1]/i').click()
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

        driver.quit()

    def Punch_out(self, driver):

        self.Log_in(driver = driver)
        time.sleep(5)

        driver.find_element(By.XPATH, '/html/body/div/header/div/div/a[1]/i').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="sign_out1"]').click()
        time.sleep(60)

        driver.quit()

    def Punch_time(self):

        dt = datetime.now().replace(tzinfo=timezone.utc)
        now = dt.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區

        week = now.weekday()
        now_without_second = str(now).split(':')[0]+':'+str(now).split(':')[1]

        if str(self.punch_in_time) in str(now_without_second) and (week != 6 and week != 5):
            return ("上班", now)
        elif str(self.punch_out_time) in str(now_without_second) and (week != 6 and week != 5):
            return ("下班", now)
        else:
            return ("不打卡", now)

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

        option = webdriver.ChromeOptions()
        option.add_argument('window-size=1024x768')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-gpu')
        option.add_argument("--headless")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        driver.set_window_size(1024, 768)

        try:
            if sign.Punch_time()[0] == '上班':
                sign.Punch_in(driver = driver)
                print(sign.Punch_time()[1], '上班打卡成功')
                continue
            elif sign.Punch_time()[0] == '下班':
                sign.Punch_out(driver = driver)
                print(sign.Punch_time()[1], '下班打卡成功')
                continue
            else:
                #print(sign.Punch_time()[1], end='\r')
                continue
        except:
            continue


if __name__ == '__main__':
    main()