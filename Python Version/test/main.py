from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def createDriver():
	options = Options()
	options.add_argument('--ignore-certificate-errors')
	options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
	#options.add_argument("--headless") # Runs Chrome in headless mode.
	options.add_argument('--no-sandbox') # Bypass OS security model
	options.add_argument('--disable-gpu')  # applicable to windows os only
	options.add_argument('start-maximized') # 
	options.add_argument('disable-infobars')
	options.add_argument("--disable-extensions")
	options.add_argument("log-level=3")
	driver = webdriver.Chrome(chrome_options=options, service_log_path="log.txt")
	return driver

def testNumSeats(numseats, expectedoutput):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element_by_name('numseats').send_keys(numseats)
    driver.find_element_by_xpath('/html/body/table/tbody/tr[1]/td[7]/button').click()
    body_text = driver.find_element_by_tag_name("body").text

    if body_text == expectedoutput:
        print('Test passed. Numseats: %s, Expected output: %s' % (numseats, expectedoutput))
    else:
        print('Test failed. Numseats: %s, Expected output: %s' % (numseats, expectedoutput))

if __name__ == '__main__':
    driver = createDriver()
    
    testNumSeats(1, 'The recommended seats are: c3')
    testNumSeats(2, 'The recommended seats are: c3 c2')
    testNumSeats(3, 'The recommended seats are: c3 c2 c1')
    testNumSeats(4, 'The recommended seats are: c2 c3 c4 c5')
    testNumSeats(5, 'The recommended seats are: c1 c2 c3 c4 c5')

    driver.close()