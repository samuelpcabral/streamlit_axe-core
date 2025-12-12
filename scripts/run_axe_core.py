import re
import os
from datetime import datetime
from selenium import webdriver
from axe_selenium_python import Axe
from selenium.webdriver.chrome.options import Options


def execute_axe_core(url, mode="desktop", device=None, width=1920, height=1080, json_log=False):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
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
    # Write results to json file for debugging
    if json_log:
        result_file = create_log_file(url)
        axe.write_results(results, result_file)
    driver.close()
    return results


def create_log_file(url):
    timestamp = datetime.now().strftime("%H:%M:%S")
    uri = re.findall(r'//([^/]+)', url)
    filename = f"{timestamp.replace(":", "-")}_{uri[0]}.json"
    filepath = os.path.join(os.getcwd(), "results", filename)
    return filepath
