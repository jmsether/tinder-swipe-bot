import numpy

from selenium import webdriver
import pickle
from time import sleep
import os.path
import json

from PIL import Image
import requests
from io import BytesIO

import glob
import os

import face_recognition

import cv2



import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from selenium.webdriver.chrome.options import Options

from secrets import username, password


class TinderBot():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\\Users\\jmset\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        PATH = "\\Users\\jmset\\PycharmProjects\\tinder-swipe-bot\\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH, options=options)

    def load_cookies(self):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        # self.driver.get('https://tinder.com')
        with open('cookietest.json', 'r', newline='') as inputdata:
            cookies = json.load(inputdata)
        curcookie = cookies[0]
        # self.driver = webdriver.Chrome()
        # driver.get("https://stackoverflow.com/")
        self.driver.add_cookie(curcookie)

    def save_cookies(self):
        # pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        cookies = self.driver.get_cookies()
        with open('cookietest.json', 'w', newline='') as outputdata:
            json.dump(cookies, outputdata)

    def phone_login(self):
        sleep(2)

        # fb_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button')
        ph_btn = self.driver.find_element_by_xpath(
            '//*[@id="q-274726726"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a')
        # fb_btn.click()
        ph_btn.click()

        ph_btn = self.driver.find_element_by_xpath(
            '//*[@id="q-53386290"]/div/div/div[1]/div/div[3]/span/div[3]/button')
        ph_btn.click()

        # switch to login popup - for facebook
        # base_window = self.driver.window_handles[0]
        # self.driver.switch_to_window(self.driver.window_handles[1])

        # email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        # email_in.send_keys(username)

        phone_in = self.driver.find_element_by_xpath('//*[@id="q-53386290"]/div/div/div[1]/div[2]/div/input')
        phone_in.send_keys(username)

        phone_in = self.driver.find_element_by_xpath('//*[@id="q-53386290"]/div/div/div[1]/button')
        phone_in.click()

        # prompt user for 2fa code

        # prompt user for email code

        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def login(self):
        self.driver.get('https://tinder.com')
        file_exists = os.path.exists('cookies.pkl')
        if file_exists:
            print("loading cookies from file")
            self.load_cookies()
        else:
            self.phone_login()

    def next_img(self):
        #bullet--active
        self.driver.find_element_by_xpath('//*[@id="q-53386290"]/div/div/div[1]/button')

    def detect_face(self, img):
        image = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_BGR2RGB)
        #image_copy = numpy.copy(image)
        image_copy = cv2.cvtColor(numpy.copy(image), cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        #haarcascade_frontalface_default
        #haarcascade_frontalface_alt2
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        face_crop = []
        for f in faces:
            x, y, w, h = [v for v in f]
            cv2.rectangle(image_copy, (x, y), (x + w, y + h), (255, 0, 0), 3)
            # Define the region of interest in the image
            face_crop.append(image_copy[y:y + h, x:x + w])
        if len(face_crop) != 1:
            return None
        for face in face_crop:
            # cv2.imshow('face', face)
            # cv2.waitKey(0)
            return Image.fromarray(face)
        return None

    def detect_face2(self, img):
        image = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_BGR2RGB)
        #image_copy = numpy.copy(image)
        image_copy = cv2.cvtColor(numpy.copy(image), cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        #haarcascade_frontalface_default
        #haarcascade_frontalface_alt2
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
        faces = face_cascade.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        face_crop = []
        for f in faces:
            x, y, w, h = [v for v in f]
            cv2.rectangle(image_copy, (x, y), (x + w, y + h), (255, 0, 0), 3)
            # Define the region of interest in the image
            face_crop.append(image_copy[y:y + h, x:x + w])
        if len(face_crop) != 1:
            return None
        for face in face_crop:
            # cv2.imshow('face', face)
            # cv2.waitKey(0)
            return Image.fromarray(face)

    def clamp(self,n, smallest, largest):
        return max(smallest, min(n, largest))

    def detect_face3(self, img):
        pad_scalar = .4
        image = numpy.asarray(img)
        image_copy = cv2.cvtColor(numpy.copy(image), cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(image)
        face_crop = []
        for (top, right, bottom, left) in faces:
            #            (image_copy, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.rectangle(image_copy, (left, top), (right, bottom), (0, 0, 255), 3)
            # Define the region of interest in the image
            pad = int((right-left)*pad_scalar)
            print("pad_scalar: " + str(pad))
            dim = image.shape
            face_crop.append(image_copy[self.clamp(top-pad,0,bottom):self.clamp(bottom+pad,0,dim[0]), self.clamp(left-pad,0,right):self.clamp(right + pad, 0,dim[1])])

        if len(face_crop) != 1:
            for face in face_crop:
                Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB)).show()
            return None
        for face in face_crop:
            # cv2.imshow('face', face)
            # cv2.waitKey(0)
            return Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))

    def get_img(self):
        # //*[@id="q-274726726"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[3]/div[1]/div[1]/span[3]/div
        # document.querySelector("#q-274726726 > div > div.App__body.H\\(100\\%\\).Pos\\(r\\).Z\\(0\\) > div > main > div.H\\(100\\%\\) > div > div > div.recsCardboard.W\\(100\\%\\).Mt\\(a\\).H\\(100\\%\\)--s.Px\\(4px\\)--s.Pos\\(r\\) > div > div > div.Toa\\(n\\).Bdbw\\(\\$recsGamepadHeight\\).Bdbw\\(\\$recsGamepadHeightDesktop\\)--ml.Bdbc\\(t\\).Bdbs\\(s\\).Bgc\\(\\#000\\).Wc\\(\\$transform\\).Prs\\(1000px\\).Bfv\\(h\\).Ov\\(h\\).W\\(100\\%\\).StretchedBox.Bdrs\\(8px\\) > div.Expand.D\\(f\\).Pos\\(r\\).tappable-view.Cur\\(p\\) > div.Expand.Pos\\(a\\).D\\(f\\).Ov\\(h\\).Us\\(n\\).keen-slider > span:nth-child(3) > div")
        #
        # img = self.driver.find_element_by_xpath('//*[@id="q-274726726"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[3]/div[1]/div[1]/span[3]/div')
        # imgpath = img.getCssValue("background-image")
        # print(imgpath)
        current_img = "Not SET"
        spans = self.get_active_card().find_elements_by_tag_name('span')
        for span in spans:
            hidden = span.get_attribute("aria-hidden")
            if 'false' == hidden:
                divs = span.find_elements_by_tag_name('div')
                for div in divs:
                    bg_url = div.value_of_css_property('background-image')
                    img_url = bg_url.lstrip('url("').rstrip('")')
                    if "https" in img_url:
                        if "/u/" in img_url:
                            # print(img_url)
                            current_img = img_url

        print(current_img)
        response = requests.get(current_img)
        # arr = numpy.asarray(bytearray(response.content), dtype=numpy.uint8)
        img = Image.open(BytesIO(response.content))
        # img = cv2.imdecode(arr, -1)
        # img.show()
        # cv_im=self.pil2cv(img)
        dt_img = self.detect_face3(img)
        if dt_img == None:
            print("no faces with normal model trying alt!")
            dt_img = self.detect_face2(img)

        if dt_img is not None:
            dt_img.show()

    def get_active_card(self):
        # recsCardboard__cards
        divs = self.driver.find_elements_by_tag_name('div')
        for div in divs:
            if "recsCardboard__cards" in div.get_attribute("class"):
                for div2 in div.find_elements_by_tag_name('div'):
                    hidden = div2.get_attribute("aria-hidden")
                    if 'false' == hidden:
                        # nonlocal cards
                        return div2

    def next_card(self):
        buttons = self.get_active_card().find_elements_by_tag_name('button')
        img_buttons = []
        # bullet D(ib) Va(m) Cnt($blank)::a D(b)::a Cur(p) bullet--active H(4px)::a W(100%)::a Py(4px) Px(2px) W(100%) Bdrs(100px)::a Bgc(#fff)::a focus-background-style
        # bullet D(ib) Va(m) Cnt($blank)::a D(b)::a Cur(p) bullet--active H(4px)::a W(100%)::a Py(4px) Px(2px) W(100%) Bdrs(100px)::a Bgc(#fff)::a focus-background-style
        current_tab = None
        for button in buttons:
            if "bullet" in button.get_attribute("class"):
                img_buttons.append(button)
                spans = button.find_elements_by_tag_name('span')
                if current_tab != None:
                    button.click()
                    break
                if "bullet--active" in button.get_attribute("class"):
                    current_tab = button.find_elements_by_tag_name('span').pop().text



        #print(len(img_buttons))
        #print("current tab is: " + current_tab)

    def get_imgs(self):
        buttons = self.get_active_card().find_elements_by_tag_name('button')
        img_buttons = []
        # bullet D(ib) Va(m) Cnt($blank)::a D(b)::a Cur(p) bullet--active H(4px)::a W(100%)::a Py(4px) Px(2px) W(100%) Bdrs(100px)::a Bgc(#fff)::a focus-background-style
        # bullet D(ib) Va(m) Cnt($blank)::a D(b)::a Cur(p) bullet--active H(4px)::a W(100%)::a Py(4px) Px(2px) W(100%) Bdrs(100px)::a Bgc(#fff)::a focus-background-style
        current_tab = None
        for button in buttons:
            if "bullet" in button.get_attribute("class"):
                img_buttons.append(button)
                spans = button.find_elements_by_tag_name('span')
                if "bullet--active" in button.get_attribute("class"):
                    current_tab = button.find_elements_by_tag_name('span').pop().text
                for span in spans:
                    print(span.text)

        print(len(img_buttons))
        print("current tab is: " + current_tab)

    def like(self):
        like_btn = self.driver.find_element_by_xpath('//button[normalize-space()="Like"]')
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath('//button[normalize-space()="Nope"]')
        dislike_btn.click()

    def auto_swipe(self):
        while True:
            sleep(0.5)
            try:
                self.like()
            except Exception:
                try:
                    self.close_popup()
                except Exception:
                    self.close_match()

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()


bot = TinderBot()
bot.login()
