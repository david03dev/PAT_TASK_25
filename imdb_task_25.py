"""
Python Selenium IMDB Search Automation with Explicit Wait and Notification Handling
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time


class IMDBSearch:
    # Chrome options for configuring the browser
    chrome_options = Options()
    chrome_options.add_argument(f"window-size={1280},{720}")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)

    def __init__(self, web_url):
        self.url = web_url

    def search(self):
        try:
            # Navigate to the IMDB name search page
            self.driver.get(self.url)

            self.driver.maximize_window()

            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")

            # Handle notification button if it appears
            try:
                # for the notification button [X]
                notification_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ipc-icon-button sc-dvXXFO hqYmDU ipc-icon-button--base ipc-icon-button--onBase']")))
                notification_button.click()  
                
                print("Clicked the notification button.")
            except Exception as e:
                print("Notification button not found or an error occurred:", e)

            # Expand all options 
            try:
                # Click on the "Expand All" button using its 'data-testid' attribute
                expand_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='adv-search-expand-all']"))
                )
                expand_button.click() 
                print("Clicked the 'Expand All' button successfully.")
            except Exception as e:
                print("Expand All button not found:", e)

            
            # Fill in the search fields
            # Enter name
            name_input = self.wait.until(EC.presence_of_element_located((By.ID, "text-input__3")))
            name_input.send_keys("Tom Cruise")
            print("Entered name: Tom Cruise")

            #  Enter minimum birth year
            birth_year_min = self.wait.until(EC.presence_of_element_located((By.ID, "text-input__10")))
            birth_year_min.send_keys("1950")
            print("Entered minimum birth year: 1950")

            birth_year_min.send_keys(Keys.TAB)

            # Enter maximum birth year
            birth_year_max = self.wait.until(EC.presence_of_element_located((By.ID, "text-input__11")))
            birth_year_max.send_keys("1970")
            print("Entered maximum birth year: 1970")
            birth_year_max.send_keys(Keys.TAB)
            
            #text-input__4
            birth_day = self.wait.until(EC.presence_of_element_located((By.ID, "text-input__4")))
            birth_day.click
            birth_day.send_keys(Keys.TAB)
                
           # Locate and click the Awards and Recognition button
            try:
                time.sleep(3)
                awards_recognition = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//button[@data-testid='test-chip-id-oscar_nominee']")))
                
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", awards_recognition)
                # Scroll to the awards recognition button
                self.driver.execute_script("arguments[0].scrollIntoView(true);", awards_recognition)

                # Ensure it is clickable before clicking
                awards_recognition = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='test-chip-id-oscar_nominee']")))
                awards_recognition.click()
                print("Clicked on the Awards and Recognition button.")
            except Exception as e:
                self.driver.execute_script("window.scrollBy(0, 200);") 
                print("Awards and Recognition button not found or not clickable:", e)


            #search with topic dropdown
            # Scroll the page until the element is visible
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", awards_recognition)
                time.sleep(3)
                topic_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='within-topic-dropdown-id']")))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", topic_dropdown)
                topic_dropdown.click()
                print("Selected Quotes in the topic dropdown.")
            except Exception as e:
                self.driver.execute_script("window.scrollBy(0, 200);") 
                print("Topic dropdown button not found or not clickable:", e)

            select_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[@class='ipc-select__input']//option[@value='QUOTES']")))
            select_dropdown.click()

            # Locate the "See results" button and click it
            see_results_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='adv-search-get-results']"))
            )
            see_results_button.click()

           
        except NoSuchElementException as e:
            print("Element not found:", e)
        finally:
            # Close the browser after the task is completed
            time.sleep(3)
            self.driver.quit()
            print("Browser closed.")


# URL of the IMDB Name Search page
url = "https://www.imdb.com/search/name/"
# Create an instance of the IMDBSearch class and perform the search
imdb_search = IMDBSearch(url)
imdb_search.search()
