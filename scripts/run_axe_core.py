import re
import os
from datetime import datetime
from selenium import webdriver
from axe_selenium_python import Axe
from selenium.webdriver.chrome.options import Options


debug_value = False


# If debug_value is True, the browser will be visible and a json file will be created with the results folder
def execute_axe_core(url, mode="desktop", device=None, width=1920, height=1080, debug=debug_value):
    chrome_options = Options()
    if not debug:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    if mode == "mobile":
        mobile_emulation = {
            "deviceName": device
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    else:
        chrome_options.add_argument(f"--window-size={width},{height}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    # Write results to json file inside results for debugging
    if debug:
        result_file = create_log_file(url)
        axe.write_results(results, result_file)
    driver.close()
    return results


# Creates log filename with timestamp and url
def create_log_file(url):
    timestamp = datetime.now().strftime("%H-%M-%S")
    uri = re.findall(r'//([^/]+)', url)
    filename = f"{timestamp}_{uri[0]}.json"
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    filepath = os.path.join(results_dir, filename)
    return filepath
