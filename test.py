import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test(login, password):
    serv = Service('./driver/chromedriver.exe')

    browser = webdriver.Chrome(service=serv)

    browser.get('https://vk.com/bookmarks?owner_id=0&post_id=0&screen=fave&type=youla_product')

    browser.find_element(By.CLASS_NAME, 'VkIdForm__input').send_keys(login)
    browser.find_element(By.CLASS_NAME, 'FlatButton.FlatButton--primary.FlatButton--size-l.FlatButton--wide.VkIdForm__button.VkIdForm__signInButton').click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div/form/div[1]/div[3]/div[1]/div/input')))
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div/form/div[1]/div[3]/div[1]/div/input').send_keys(password)
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div/form/div[2]/button').click()

    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'thumbed_link__button.flat_button')))

    for i in range(4):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'thumbed_link__button.flat_button')))
    buttons_elements = browser.find_elements(By.CLASS_NAME, 'thumbed_link__button.flat_button')

    ads_urls = []

    for button_element in buttons_elements:
        url = button_element.get_attribute('href')

        ads_urls.append(url)

    print(len(ads_urls))

test('ulyh5x6fh1zx@1secmail.com', 'auenegr2289')