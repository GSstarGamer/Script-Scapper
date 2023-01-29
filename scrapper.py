from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import PyUtls as utils
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep as wait


try:
    utils.os.system('taskkill /F /IM Firefox.exe')
except:
    pass

utils.clear()


key = utils.binput('keyword: ')
threads = int(utils.binput('max threads: '))

list_of_scripts = []

def scrape_page(url):
    utils.bprint(f'Looking in {url}')
    options = FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*")))
    except TimeoutError:
        driver.quit()
        utils.error(f'{url} took too long to load, browser window killed')
        return
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    scripts = re.findall(r'loadstring\(game:HttpGet\((.*)\)\)\(\);?', soup.get_text())
    if scripts:
        for script in scripts:
            script = script.replace('”', '"').replace('“', '"').replace(' ', ' ').replace('‘', '"').replace('’', '"').replace("'", '"').replace("'", '"')
            script = f'loadstring(game:HttpGet({script}))();'
            if script not in list_of_scripts:
                utils.success(f'Found script in {url} - {script}')
                list_of_scripts.append(script)
                with open(f'scripts-{key}.txt', 'a') as f:
                    f.write(script+'\n')
            else:
                utils.fail(f'Found script in {url} - {script} but dupe')
    else:
        driver.close()
        utils.fail(f'Got None with {url}')

def search(query):
    utils.clear()
    utils.bprint('Starting search...')
    options = FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(f'https://duckduckgo.com/?q={query}')
    utils.bprint('Opened Browser')
    
    while True:
        try:
            more_results_element = driver.find_elements('xpath', "//a[text()='More results']")
            loading_indicator = driver.find_elements('xpath', "//*[@id='links']/span")
            if more_results_element and not loading_indicator:
                utils.bprint('Extending search results')
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable(more_results_element[0]))
                more_results_element[0].click()
                driver.implicitly_wait(3)
            else:
                utils.bprint('End of search results or slow internet')
                break
        except StaleElementReferenceException:
            pass



    utils.bprint('Getting links...')
    links = driver.find_elements("xpath", "//a[@href]")

    list_links = []
    for i in links:
        if i.get_attribute('href') not in list_links:
            if i.get_attribute('href').find('duckduckgo') == -1 and i.get_attribute('href') != 'javascript:;' and i.get_attribute('href').find('spreadprivacy') == -1:
                list_links.append(i.get_attribute('href'))
                utils.success(f'Good url')
        else:
            utils.fail('Dupe url found')

    utils.bprint(f'Got {len(list_links)} links.')
    wait(3)
    driver.close()


    utils.bprint('Closing browser')

    utils.clear()
    utils.bprint('Starting crawler...')
    with ThreadPoolExecutor(max_workers=threads) as e:
        for link in list_links:
            try:
                e.submit(scrape_page, link)
            except:
                utils.error(f'{link} failed')
    



search(key)
utils.success('Done :sunglasses:')