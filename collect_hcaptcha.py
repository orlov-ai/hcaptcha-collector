import os
import sys
import time
from datetime import datetime
from io import BytesIO

from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from seleniumwire import webdriver
from tqdm import tqdm

if 'HCAPTCHA_DATASET_PATH' not in os.environ:
    print('please set HCAPTCHA_DATASET_PATH environment variable')
    sys.exit(1)
output_path = os.environ['HCAPTCHA_DATASET_PATH']
ff_options = FirefoxOptions()
ff_options.headless = False

driver = webdriver.Firefox(options=ff_options)
driver.set_window_size(1366, 768)

time.sleep(5)


class Filesystem:
    def __init__(self, main_folder):
        self.main_folder = main_folder
        os.makedirs(self.main_folder, exist_ok=True)
        self.c_folder = 0
        self.c_subfolder = 0
        self.limit_folders = 1000
        self.limit_subfolders = 1000

        self.date_hour = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.folder = "{}/{}/{}".format(self.main_folder, self.date_hour, self.c_folder)
        os.makedirs(self.folder)

    def set_current_folder(self):
        if self.c_subfolder >= self.limit_subfolders:

            self.c_folder += 1
            self.c_subfolder = 0
            self.folder = "{}/{}/{}".format(self.main_folder, self.date_hour, self.c_folder)
            if self.c_folder < self.limit_folders:
                os.makedirs(self.folder)

        if self.c_folder >= self.limit_folders:
            self.c_folder = 0
            self.date_hour = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            self.folder = "{}/{}/{}".format(self.main_folder, self.date_hour, self.c_folder)
            os.makedirs(self.folder)

    def write_pic(self, pics, text: str):
        self.set_current_folder()
        prefix = str(int(time.time() * 1000))
        very_current_folder = self.folder + '/' + prefix
        os.makedirs(very_current_folder, exist_ok=True)
        path_text = very_current_folder + '/text.txt'
        with open(path_text, 'w') as f:
            f.write(text)
        for i, pic in enumerate(pics):
            path_pic = very_current_folder + f'/{i}.jpg'
            with open(path_pic, 'w') as f:
                pic.save(f, format='jpeg')


filesystem = Filesystem(output_path)
for i in tqdm(range(1000000)):
    try:
        driver.get('http://test.mydomain.com:5000')
        time.sleep(4)
        del driver.requests

        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[0])
        driver.find_element(By.ID, 'checkbox').click()

        time.sleep(4)
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[1])
        prompt_text = driver.find_element(By.CLASS_NAME, 'prompt-text')

        pic_requests = [x for x in driver.requests if 'https://imgs.hcaptcha.com/' in x.url]
        pics = [Image.open(BytesIO(x.response.body)) for x in pic_requests]
        filesystem.write_pic(pics=pics, text=prompt_text.text)
        if i % 10 == 0:
            driver.delete_all_cookies()
        filesystem.c_subfolder += 1
        time.sleep(1)
    except KeyboardInterrupt:
        break
    except Exception as err:
        print(err)
        time.sleep(300)
