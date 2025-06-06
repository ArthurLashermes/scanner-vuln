from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome en headless ou non selon besoin
options = Options()
options.headless = True  # Mettre False si tu veux voir le navigateur

driver = webdriver.Chrome(options=options)

try:
    url = "http://127.0.0.1:5000/xss?name=<script>alert('XSS')</script>"
    driver.get(url)

    try:
        # Attendre jusqu'à ce qu'une alerte apparaisse (max 5 sec)
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("XSS vulnerability detected! Alert text:", alert.text)
        alert.accept()
    except TimeoutException:
        print("No XSS alert popup detected.")
finally:
    driver.quit()
