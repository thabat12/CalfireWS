from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome()
driver.get('https://nowdata.rcc-acis.org/sto/')
time.sleep(5)
a = driver.find_elements_by_tag_name('input')
print(driver.find_elements_by_id('results_area'))
for i in a:
    try:
        if i.get_attribute('value') == 'StnProduct_monavg':
            i.click()
    except:
        print('error occured')
b = driver.find_elements_by_tag_name('input')
for i in b:
    if i.get_attribute('title') == '4-digit starting year (\'por\' for first year of record)':
        i.clear()
        i.send_keys('2013')
        continue
    if i.get_attribute('title') == '4-digit ending year (\'por\' for last year of record':
        i.clear()
        i.send_keys('2020')
c = driver.find_elements_by_tag_name('option')
for i in c:
    if i.get_attribute('value') == 'avgt':
        i.click()

    if i.get_attribute('value') == 'mean':
        i.click()
# now the table and charts are loaded into the html
driver.find_element_by_id('go').click()
time.sleep(3)
test = driver.find_elements_by_tag_name('tr')
data = {}
for i in test[1:3]:
    print(i.get_attribute('innerHTML'))
    elements = i.find_elements_by_tag_name('td')
    data[int(elements[0].get_attribute('innerHTML'))] = [float(i.get_attribute('innerHTML')) if i.get_attribute('innerHTML') != 'T' else 0 \
                                                         for i in elements[1:]]



