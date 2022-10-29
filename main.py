import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os

def txt_reader(file_path):
    with open(file_path, 'r') as file:
        all_lines = file.readlines()

    login_and_password = all_lines[0]
    login_and_password = login_and_password.split(':')

    login = login_and_password[0]
    password = login_and_password[1]

    return login, password

def csv_reader(file_path):
    url_list = []

    with open(file_path) as file:
        all_lines = file.readlines()
        all_lines = all_lines[1:]

        for line in all_lines:
            line_list = line.split(';')

            url = line_list[5]
            url = url.replace('"', '')

            url_list.append(url)

    return url_list

def licke_engine():
    csv_path = input('Введите путь к csv файлу с url: ')
    txt_path = input('Введите путь к фалу с данными от ВК: ')

    login, password = txt_reader(txt_path)

    serv = Service('./driver/chromedriver.exe')

    browser = webdriver.Chrome(service=serv)

    #Авторизация в ВК
    browser.get('https://vk.com/')

    browser.find_element(By.CLASS_NAME, 'VkIdForm__input').send_keys(login)
    browser.find_element(By.XPATH, '/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/div/form/button[1]').click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div/form/div[1]/div[3]/div[1]/div/input')))
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div/form/div[1]/div[3]/div[1]/div/input').send_keys(password)
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div/form/div[2]/button').click()


    youla_url_list = csv_reader(csv_path)

    # Работа с юлой

    first_url_flag = True

    for youla_url in youla_url_list:
        if first_url_flag == True:
            try:
                browser.switch_to.new_window('tab2')

                browser.get(youla_url_list[0])

                browser.find_element(By.CLASS_NAME, 'sc-jlqnSw.hoxkWD').click()
                WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/form/div[4]/button')))
                browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/form/div[4]/button').click()

                WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'sc-jlqnSw.hoxkWD')))

                time.sleep(1)

                browser.close()

                browser.switch_to.window(browser.window_handles[0])

                first_url_flag = False
            except:
                continue

        elif first_url_flag == False:
            try:
                browser.switch_to.new_window('tab2')

                browser.get(youla_url)

                WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sc-jlqnSw.hoxkWD')))
                browser.find_element(By.CLASS_NAME, 'sc-jlqnSw.hoxkWD').click()

                time.sleep(0.5)

                browser.close()

                browser.switch_to.window(browser.window_handles[0])
            except:
                continue

def vk_engine():
    txt_path = input('Введите путь к фалу с данными от ВК: ')

    login, password = txt_reader(txt_path)

    serv = Service('./driver/chromedriver.exe')

    browser = webdriver.Chrome(service=serv)

    browser.get('https://vk.com/bookmarks?owner_id=0&post_id=0&screen=fave&type=youla_product')

    browser.find_element(By.CLASS_NAME, 'VkIdForm__input').send_keys(login)
    browser.find_element(By.CLASS_NAME, 'FlatButton.FlatButton--primary.FlatButton--size-l.FlatButton--wide.VkIdForm__button.VkIdForm__signInButton').click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div/form/div[1]/div[3]/div[1]/div/input')))
    browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[2]/div/div/div/form/div[1]/div[3]/div[1]/div/input').send_keys(password)
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

    for ads_url in ads_urls:
        browser.switch_to.new_window('tab2')

        browser.get(ads_url)

        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[15]/div/div[1]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[2]/button[1]')))
        browser.find_element(By.XPATH, '/html/body/div[15]/div/div[1]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[2]/button[1]').click()
        time.sleep(0.5)
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[17]/div[2]/div[2]/div[2]/button[2]')))
        browser.find_element(By.XPATH, '/html/body/div[17]/div[2]/div[2]/div[2]/button[2]').click()
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[17]/div[2]/div[3]/button')))
        browser.find_element(By.XPATH, '/html/body/div[17]/div[2]/div[3]/button').click()

        time.sleep(1.5)

        browser.close()

        browser.switch_to.window(browser.window_handles[0])

def main():
    os.system('cls')

    print('''
                        Powered by:
                        
 .d8888b.        d8888 88888888888 .d88888b.   .d8888b.  888     888 
d88P  Y88b      d88888     888    d88P" "Y88b d88P  Y88b 888     888 
Y88b.          d88P888     888    888     888 888    888 888     888 
 "Y888b.      d88P 888     888    888     888 888        888     888 
    "Y88b.   d88P  888     888    888     888 888        888     888 
      "888  d88P   888     888    888     888 888    888 888     888 
Y88b  d88P d8888888888     888    Y88b. .d88P Y88b  d88P Y88b. .d88P 
 "Y8888P" d88P     888     888     "Y88888P"   "Y8888P"   "Y88888P"
 
                    Tg: https://t.me/SATOCCU
 ''')

    print(f'\n\nМеню:\n'
          f'1.Утилита для добавления объявлений в избранное\n'
          f'2.Утилита для отправки сообщения в ВК')

    select_utils = input('')

    if select_utils == '1':
        os.system('cls')

        try:
            licke_engine()
        except Exception as error:
            print(error)
    else:
        os.system('cls')

        try:
            vk_engine()
        except Exception as error:
            print(error)

while True:
    main()