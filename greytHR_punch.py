import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- GET CREDENTIALS FROM GITHUB SECRETS ---
GREYTHR_URL = os.environ["GREYTHR_URL"]
USERNAME = os.environ["GREYTHR_USER"]
PASSWORD = os.environ["GREYTHR_PASS"]

def punch_attendance():
    # --- HEADLESS CHROME SETUP (REQUIRED FOR CLOUD) ---
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless") # No GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 30)

    try:
        print("1. Opening GreytHR...")
        driver.get(GREYTHR_URL)

        print("2. Entering Credentials...")
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", login_btn)

        print("3. Waiting for Dashboard...")
        time.sleep(15) 

        # Handle Popups
        try:
            close_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'close') or contains(@class, 'cancel')]")
            for btn in close_buttons:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
        except:
            pass 

        print("4. Searching for Punch Button...")
        # Universal Search
        targets = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sign In') or contains(text(), 'Sign Out') or contains(text(), 'Web Punch')]")
        
        clicked = False
        for t in targets:
            if t.is_displayed():
                print(f"   -> Clicking: {t.text}")
                driver.execute_script("arguments[0].click();", t)
                clicked = True
                break
        
        if not clicked:
            # Fallback for <gt-button>
            gt_btn = driver.find_element(By.TAG_NAME, "gt-button")
            driver.execute_script("arguments[0].click();", gt_btn)

        print(">>> SUCCESS: Action Performed")
        time.sleep(5)

    except Exception as e:
        print(f"ERROR: {e}")
        # Print page source if error helps debugging
        # print(driver.page_source) 

    finally:
        driver.quit()

if __name__ == "__main__":
    punch_attendance()