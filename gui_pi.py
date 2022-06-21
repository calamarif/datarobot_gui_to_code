# Author: Callum Finlayson (callum@datarobot.com)
# Date: 15 June 2022
# Desc:  "GUI PI" - Workaround for the API not having a suitable variable to cater for "optional features"
# Last Updated Date: 21 June 2022

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import time
import os
from dotenv import load_dotenv #installed with "python-dotenv"
from pathlib import Path

def main():
    # Create a ".env" file 
    dotenv_path = Path('./.env')
    load_dotenv(dotenv_path=dotenv_path)

    #Variables we will need    
    DATAROBOT_URL=os.getenv('DATAROBOT_URL')
    USERNAME=os.getenv('USERNAME')
    PASSWORD=os.getenv('PASSWORD')
    DATASET_FILE_PATH=os.getenv('DATASET_FILE_PATH')
    OPTIONAL_FEATURES_COLUMN =os.getenv('OPTIONAL_FEATURES_COLUMN')
    PROJECT_NAME=os.getenv('PROJECT_NAME')
    CLEANUP_FLAG = os.getenv('CLEANUP_FLAG')
    USE_AICAT_FLAG = os.getenv('USE_AICAT_FLAG')
    AICAT_ITEM_NAME = os.getenv('AICAT_ITEM_NAME')
    
    # Get the directory and file name from the full path provided
    download_dir = os.path.dirname(os.path.abspath(DATASET_FILE_PATH))
    ai_catalog_file = (os.path.basename(DATASET_FILE_PATH))

    # Start the webdriver
    options = Options()
    # Set this to false if you want to see the browser do it's thing (useful for editing this script)
    options.headless = False
    # Set some options here so the results will be downloaded to the dir
    options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
    driver.get(DATAROBOT_URL)
    time.sleep(10) # there is probably a more elegant way to achieve this
    # This is important to do for the success of selecting the correct project
    driver.maximize_window()

    #This is the beginning of the interaction with the DataRobot website.
    # Login
    driver.find_element(by=By.XPATH, value = "//*[@id=\"email\"]").send_keys(USERNAME)
    driver.find_element(by=By.XPATH, value = "//*[@id=\"password\"]").send_keys(PASSWORD)
    driver.find_element(by=By.XPATH, value = "//*[@id=\"datarobot\"]/div/div[2]/div[3]/div/div[2]/form/button").click()
    time.sleep(3)

    # Folder pop up and select "Manage Projects"
    delay = 5 # seconds
    try:
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'IdOfMyElement')))
    except TimeoutException as e:
        print (e)

    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"navigation-user\"]/div/div[1]/button"))).click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value ="//*[@id=\"react-pop\"]/div/div/div/ul/li/a").click()

    # Click "Manage Projects" and loop through the projects until PROJECT_NAME and click
    i=1
    try:
        time.sleep(1) 
        project = driver.find_element(by=By.XPATH, value ="/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div/ui-view/react-ui-view-adapter/div/div/div/div[2]/div[2]/div["+str(i)+"]/div[2]")
        while (project):
            print(project.text)
            if project.text == PROJECT_NAME:
                project.click()
                print("Project Selected - " + project.text)
            i+=1
            time.sleep(1) # this sleep is important to wait for the correct project to be selected, it takes a second to dynamically refresh
            project = driver.find_element(by=By.XPATH, value ="/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div/ui-view/react-ui-view-adapter/div/div/div/div[2]/div[2]/div["+str(i)+"]/div[2]")                
            time.sleep(1)    
    except NoSuchElementException:
        print ("no more projects")
    time.sleep(5)

    #Click on the "Models" tab
    models_tab= driver.find_elements(by=By.XPATH, value ="//*[@id=\"navigation-primary\"]/ul/li[5]/a")
    for my_href in models_tab:
        project_url = (my_href.get_attribute("href"))
    driver.get(project_url)
    time.sleep(5)

    #Expand the top model (the logic could be enhanced here to loop through all models and have the script search for a specific name)
    delay = 3 # seconds
    try:
        #element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/div[1]/div/leaderboard-item/div/div[1]/div[1]/div[2]/span[1]")))
        element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div/div/div[1]/div[2]")))
        driver.execute_script("arguments[0].click();", element)
    except TimeoutException as e:
        print (e)    
    
    try:
        element.click()
    except:
        print("couldn't expand top mode")
    
    time.sleep(5) # This is a bit long, but important for latency issues (might need to increase on slow connections)
    # Click on the 'Predict' tab    
    #element = driver.find_element(by=By.XPATH, value = "/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/div[1]/div/leaderboard-item/div/div[2]/div[1]/button[4]")
    element = driver.find_element(by=By.XPATH, value = "/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div[1]/div[2]/div[1]/button[4]")
    driver.execute_script("arguments[0].click();", element)

    time.sleep(2)
    # Sometimes there is an existing item in the "optionall features" text box, the below command will remove it if it exists
    try:
        #element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/div[1]/div/div/div/ui-view/react-ui-view-adapter/div/div[2]/div/div[1]/div[2]/div/div/div/span/button")))
        element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div[2]/div/ui-view/ui-view/react-ui-view-adapter/div/div[2]/div/div[1]/div[2]/div/div/div/span/button")))
        element.click()
        time.sleep(2) # This is important to wait for the item to be removed
    except:
        # no problem if this doesn't exist, most times it won'!
        pass
    
    #Enter the "Optional Features" (want to add the OPTIONAL_FEATURES_COLUMN)                                             
    #optional_features_box = driver.find_element(by=By.XPATH, value ="/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/div[1]/div/div/div/ui-view/react-ui-view-adapter/div/div/div/div[1]/div[2]/div/div/div/div/div/input")
    #optional_features_box = driver.find_element(by=By.XPATH, value ="/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div[2]/div/ui-view/ui-view/react-ui-view-adapter/div/div[2]/div/div[1]/div[2]/div/div/div/div/div/input")
                                                                     
    #optional_features_box = driver.find_element(by=By.XPATH, value ="/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div[2]/div/ui-view/ui-view/react-ui-view-adapter/div/div[2]/div/div[1]/div[2]/div/div/div/span/span[2]")
    optional_features_box = driver.find_element(by=By.XPATH, value ="/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div[2]/div/ui-view/ui-view/react-ui-view-adapter/div/div[2]/div/div[1]/div[2]/div/div/div/div/div/input")
    time.sleep(2)

    # Send the optional feature (or comma separated list of features if you want more than one)
    optional_features_box.send_keys(OPTIONAL_FEATURES_COLUMN)
    time.sleep(2)

    # Need to press "Enter" to confirm the column
    optional_features_box.send_keys(u'\ue007')
    time.sleep(1)

    # "Choose File" drop down
    #driver.find_element(by=By.XPATH, value ="//*[@id=\"lid-62a1d0ec3724060f13f90f78\"]/div/div/div/ui-view/react-ui-view-adapter/div/div[2]/div/div[2]/div/div[1]/div/button").click()
    driver.find_element(by=By.XPATH, value ="/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div[2]/div/ui-view/ui-view/react-ui-view-adapter/div/div[2]/div/div[2]/div/div[1]/div/button").click()
    time.sleep(1)
    if USE_AICAT_FLAG:

        # OPTION1: AI Catalog option popup
        driver.find_element(by=By.XPATH, value ="//*[@id=\"dropdown-item-AI_CATALOG\"]/button").click()
        time.sleep(1)
        i=1
        try:
            #Loop through the AI catalog items (if it's not in the first page it will fail)
            while (driver.find_element(by=By.XPATH, value ="/html/body/div[19]/div/div/div/div/div/div[2]/div[3]/div["+str(i)+"]")):
                time.sleep(1)
                ai_cat_item = driver.find_element(by=By.XPATH, value ="/html/body/div[19]/div/div/div/div/div/div[2]/div[3]/div["+str(i)+"]/div/div/header/div/span[1]")
                print(ai_cat_item.text)
                if ai_cat_item.text == AICAT_ITEM_NAME:
                    #Click on the correct item in the popup
                    try:
                        time.sleep(2)
                        #ai_cat_button = driver.find_elements(by=By.XPATH, value ="/html/body/div[19]/div/div/div/div/div/div[2]/div[3]/div["+str(i)+"]/div/div")
                        ai_cat_button = driver.find_element(by=By.XPATH, value ="/html/body/div[19]/div/div/div/div/div/div[2]/div[3]/div["+str(i)+"]/div")
                        ai_cat_button.click()
                    except:
                        if i == 1:
                            ai_cat_button = driver.find_element(by=By.XPATH, value ="/html/body/div[19]/div/div/div/div/div/div[2]/div[3]/div")
                        else:
                            ai_cat_button = driver.find_element(by=By.XPATH, value ="/html/body/div[19]/div/div/div/div/div/div[2]/div[3]/div["+str(i)+"]")
                        print ("did't click anything on the AU Catalog popup")
                    time.sleep(2)
                    #Click the button "use this dataset"
                    use_this_dataset_button = driver.find_element(by=By.XPATH, value ="/html/body/div[19]/div/div/div/div/aside/div[1]/span/button")
                    use_this_dataset_button.click()
                i+=1
                time.sleep(1)
        except NoSuchElementException:
            print ("no more ai catalog items, went through " + str(i) +" iterations")

    else:

        # Local File option only for now (clicking this will cause a file selector popup)
        driver.find_element(by=By.XPATH, value ="//*[@id=\"dropdown-item-LOCAL\"]/label").click()
        time.sleep(2)

        # Select the file for the file selector pop up
        driver.find_element(by=By.XPATH, value ="//*[@id=\"LOCAL\"]").send_keys(DATASET_FILE_PATH)

    time.sleep(2)
    delay = 100     # This delay is set to a high number to cater for large files taking a while to upload
    # Click "Compute Predictions"
    # I ended up using nth-of-type(2) where a value of 1 wou    ld be the training set, but it seems to time out sometimes, so setting the XPATH method as a backup plan (ie in the excaption block)
    try:
        element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button[test-id=compute-predictions-button]:nth-of-type(2)")))    
    except:
        # Set to not timeout
        element = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/div[1]/div/div/div/ui-view/react-ui-view-adapter/div/div[2]/div/div[3]/div[1]/aside/div/button[2]")
    
    time.sleep(10) # need to delay it being clickable and clicking on it (which seems strange)    
    element.click()

    # The below call i have added in exasperation as couldn't work out how to make the WebDriverWait to wait
    time.sleep(100) 

    #DOWNLOAD RESULTS
    delay = 200 # Again have set this to a relatively high number in case it takes a long time to compute the predictions
    # Wait until "Download Predictions" is displayed (and ready to be clicked).. Making the assumption of no duplicate projects
    try:
        # Can't use CSS_SELECTOR here because there are possibly other "Download Prediction" elements on page. Although XPATH appears to change... This is possibly a problem
        #element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button[test-id=download-predictions-button]:first-child")))
        #element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/div[1]/div/div/div/ui-view/react-ui-view-adapter/div/div[2]/div/div[3]/div[1]/aside[2]/div/button[2]/span')))                                                                                            
        #element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div[2]/div/ui-view/ui-view/react-ui-view-adapter/div/div[2]/div/div[2]/div/div[1]/div/button')))
        element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div[2]/div/ui-view/ui-view/react-ui-view-adapter/div/div[2]/div/div[3]/div[1]/aside[2]/div/button[2]')))
        time.sleep(2)
        element.click()
        print("Predicitons Exported to - " + str(DATASET_FILE_PATH))
        if CLEANUP_FLAG:       
            # Selecting the delete button for the top "Prediction Dataset"
            #delete_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/div[1]/div/div/div/ui-view/react-ui-view-adapter/div/div[2]/div/div[3]/div[1]/aside[2]/div/button[3]")
            delete_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/section/section/react-ui-view-adapter/div[2]/ui-view/react-ui-view-adapter/div/div/div[2]/ui-view/leaderboard/div/div/div/leaderboard-rows/div/div[1]/div/div[2]/div/ui-view/ui-view/react-ui-view-adapter/div/div[2]/div/div[3]/div[1]/aside[2]/div/button[3]")
            time.sleep(20) # Give time to download, then cleanup
            delete_button.click()
            time.sleep(2)
            delete_confirm = driver.find_element(By.XPATH, "/html/body/div[19]/div/div/footer/button[1]")
            time.sleep(2)
            delete_confirm.click()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # load the variables from the .env file
    load_dotenv()
    # run the script
    main()