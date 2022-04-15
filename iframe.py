from selenium import webdriver
from selenium.webdriver.common.by import By


def find_iframe(link):
    driver = webdriver.Chrome()
    driver.get(link)
    driver.implicitly_wait(3)
    iframe_list = driver.find_elements(By.TAG_NAME, 'iframe')
    if len(iframe_list) > 0:
        iframe_links_list = []
        for iframe in iframe_list:
            if iframe.get_attribute('src') != '':
                iframe_links_list.append(iframe.get_attribute('src'))
        driver.close()
        return 'Тэг iframe:', iframe_links_list
