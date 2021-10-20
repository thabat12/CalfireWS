from selenium import webdriver
from geopy.geocoders import Nominatim
from webdriver_manager.chrome import ChromeDriverManager
import time


# give a list of years to find the precipitation values and it will return a dictionary object with everything

area_codes = ['sgx', 'lox', 'hnx', 'mtr', 'eka', 'mfr', 'rev']

'''
{
'locale': name,
'long': long,
'lat': lat,
'precip': precip,
'avg_temp' : avg_temp,
}
'''

# get the browser running
driver = webdriver.Chrome()
driver.get(f'https://nowdata.rcc-acis.org/{area_codes[-1]}/')

# initialize the geopy module
geo = Nominatim(user_agent='hello')


elem = driver.find_element_by_tag_name('select')

print(elem)

# have to give time to load so html renders properly
time.sleep(1)

locale_list = elem.find_elements_by_tag_name('option')
locale_list = list(filter(lambda x: 'CA' in x.get_attribute('innerHTML'), locale_list))


overall_data = []


# O(N^6) but doesn't matter since there's no other way
for locale_elem in locale_list:

    if len(overall_data) > 9:
        break

    locale_name = locale_elem.get_attribute('innerHTML')

    try:
        location = geo.geocode(locale_name)
    except:
        print('geolocation error')
        break

    print('at', locale_name)

    locale_elem.click()

    time.sleep(1)

    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[1]/button[3]').click()
        overall_data.pop(-1)
    except:
        pass

    # for montly summarized data
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/label[3]/input').click()
    # start date input
    driver.find_element_by_xpath('//*[@id="year_area"]/fieldset/input[1]').clear()
    driver.find_element_by_xpath('//*[@id="year_area"]/fieldset/input[1]').send_keys('2013')
    # end date input
    driver.find_element_by_xpath('//*[@id="year_area"]/fieldset/input[2]').clear()
    driver.find_element_by_xpath('//*[@id="year_area"]/fieldset/input[2]').send_keys('2020')
    # precipitation
    driver.find_element_by_xpath('//*[@id="element_area"]/fieldset[1]/select/option[4]').click()
    # mean selection
    driver.find_element_by_xpath('//*[@id="element_area"]/fieldset[2]/select/option[2]').click()
    # submit the query
    driver.find_element_by_xpath('//*[@id="go"]').click()

    time.sleep(1)

    t_body = None

    try:
        t_body = driver.find_element_by_xpath('//*[@id="results_area"]/table/tbody')
    except:
        # too many edge cases
        continue


    tr_elems = t_body.find_elements_by_tag_name('tr')


    precip_map = {}

    for tr in tr_elems:

        year_vals = []

        td = tr.find_elements_by_tag_name('td')

        cur_year = int(td[0].get_attribute('innerHTML'))

        for data in td[1:-1]:

            try:
                year_vals.append(float(data.get_attribute('innerHTML')))
            except:
                year_vals.append(0)

        precip_map[cur_year] = year_vals

    # I will also get rid of the average temperatures this way as well
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/button[3]').click()
    # for montly summarized data
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/label[3]/input').click()
    # start date input
    driver.find_element_by_xpath('//*[@id="year_area"]/fieldset/input[1]').clear()
    driver.find_element_by_xpath('//*[@id="year_area"]/fieldset/input[1]').send_keys('2013')
    # end date input
    driver.find_element_by_xpath('//*[@id="year_area"]/fieldset/input[2]').clear()
    driver.find_element_by_xpath('//*[@id="year_area"]/fieldset/input[2]').send_keys('2020')
    # average temperature
    driver.find_element_by_xpath('//*[@id="element_area"]/fieldset[1]/select/option[3]').click()
    # mean selection
    driver.find_element_by_xpath('//*[@id="element_area"]/fieldset[2]/select/option[2]').click()
    # submit the query
    driver.find_element_by_xpath('//*[@id="go"]').click()

    time.sleep(1)

    t_body = None

    try:
        t_body = driver.find_element_by_xpath('//*[@id="results_area"]/table/tbody')
    except:
        continue

    tr_elems = t_body.find_elements_by_tag_name('tr')

    temp_map = {}

    for tr in tr_elems:

        year_vals = []

        td = tr.find_elements_by_tag_name('td')

        cur_year = int(td[0].get_attribute('innerHTML'))

        for data in td[1:-1]:

            try:
                year_vals.append(float(data.get_attribute('innerHTML')))
            except:
                year_vals.append(0)

        temp_map[cur_year] = year_vals




    try:
        insert_data = {
            'name' : locale_name,
            'long' : location.longitude,
            'lat' : location.latitude,
            'precip_years' : precip_map,
            'temp_map' : temp_map
        }

        overall_data.append(insert_data)

        print(insert_data)
    except:
        continue



    # close the window to prepare for the next iteration
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/button[3]').click()

print(overall_data)