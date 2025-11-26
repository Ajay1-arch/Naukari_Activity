#! python3
# -*- coding: utf-8 -*-
"""
Naukri Daily Update Automation - Main Script
Uses configuration management and secrets from config/
"""

import io
import logging
import os
import sys
import time
from datetime import datetime
from random import choice, randint
from string import ascii_uppercase, digits
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# Import configuration and secrets
from config_loader import get_secrets, get_config

# Load secrets and config
secrets = get_secrets()
config = get_config()

# Get credentials from secrets
username = secrets.get('naukri.username')
password = secrets.get('naukri.password')
mob = secrets.get('naukri.mobile')
originalResumePath = secrets.get('paths.original_resume')
modifiedResumePath = secrets.get('paths.modified_resume')

# Get settings from config
updatePDF = config.get('Settings', 'UPDATE_PDF', var_type=bool)
headless = config.get('Settings', 'HEADLESS', var_type=bool)
upload_resume = config.get('Settings', 'UPLOAD_RESUME', var_type=bool)
update_profile = config.get('Settings', 'UPDATE_PROFILE', var_type=bool)

# Get URLs from config
NAUKRI_LOGIN_URL = config.get('URLs', 'NAUKRI_LOGIN_URL')
NAUKRI_PROFILE_URL = config.get('URLs', 'NAUKRI_PROFILE_URL')

# Setup logging
log_file = Path(__file__).parent.parent / config.get('Logging', 'LOG_FILE')
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename=str(log_file),
    format="%(asctime)s : %(message)s"
)

# Environment variables
os.environ["WDM_LOCAL"] = "1"
os.environ["WDM_LOG_LEVEL"] = "0"

# Profile headline variations
PROFILE_HEADLINES = [
    "Data Engineer | BigQuery | Cloud Composer | Python | SAP BODS",
    "GCP Certified Senior Data Engineer | Cloud Analytics | AI/ML",
    "Data Pipeline Expert | Airflow | Talend | Cloud Architecture",
    "BigQuery Specialist | ETL/ELT | Data Lakehouse | Cloud Solutions",
    "Cloud Data Engineer | Tableau | Power BI | Analytics | GCP/Azure",
    "Data Engineering Lead | SQL | PySpark | Enterprise Solutions",
    "Analytics Engineer | Cloud-Native | Data Quality | Business Intelligence",
    "Senior Data Engineer | SAP Migration | Financial Analytics | Healthcare",
    "Data Architect | Cloud Platforms | 3+ YRS | Team Lead | AI-Assisted Dev",
    "BigQuery Expert | Python | SQL | AI-Driven Analytics | 400+ Users Supported",
]


def log_msg(message):
    """Print to console and store to Log"""
    print(message)
    logging.info(message)


def catch(error):
    """Method to catch errors and log error details"""
    _, _, exc_tb = sys.exc_info()
    lineNo = str(exc_tb.tb_lineno)
    msg = "%s : %s at Line %s." % (type(error), error, lineNo)
    print(msg)
    logging.error(msg)


def getObj(locatorType):
    """This map defines how elements are identified"""
    map = {
        "ID": By.ID,
        "NAME": By.NAME,
        "XPATH": By.XPATH,
        "TAG": By.TAG_NAME,
        "CLASS": By.CLASS_NAME,
        "CSS": By.CSS_SELECTOR,
        "LINKTEXT": By.LINK_TEXT,
    }
    return map[locatorType.upper()]


def GetElement(driver, elementTag, locator="ID"):
    """Wait max 15 secs for element and then select when it is available"""
    try:
        def _get_element(_tag, _locator):
            _by = getObj(_locator)
            if is_element_present(driver, _by, _tag):
                return WebDriverWait(driver, 15).until(
                    lambda d: driver.find_element(_by, _tag)
                )

        element = _get_element(elementTag, locator.upper())
        if element:
            return element
        else:
            log_msg("Element not found with %s : %s" % (locator, elementTag))
            return None
    except Exception as e:
        catch(e)
    return None


def is_element_present(driver, how, what):
    """Returns True if element is present"""
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def WaitTillElementPresent(driver, elementTag, locator="ID", timeout=30):
    """Wait till element present. Default 30 seconds"""
    result = False
    driver.implicitly_wait(0)
    locator = locator.upper()

    for _ in range(timeout):
        time.sleep(0.99)
        try:
            if is_element_present(driver, getObj(locator), elementTag):
                result = True
                break
        except Exception as e:
            log_msg("Exception when WaitTillElementPresent : %s" % e)
            pass

    if not result:
        log_msg("Element not found with %s : %s" % (locator, elementTag))
    driver.implicitly_wait(3)
    return result


def ci(xpath_part: str) -> str:
    """
    Wraps an XPath string in lowercase translate() for case-insensitive matching.
    """
    return f"translate({xpath_part},'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"


def tearDown(driver):
    try:
        driver.close()
        log_msg("Driver Closed Successfully")
    except Exception as e:
        catch(e)
        pass

    try:
        driver.quit()
        log_msg("Driver Quit Successfully")
    except Exception as e:
        catch(e)
        pass


def get_random_headline():
    """Get a random profile headline from the list"""
    return choice(PROFILE_HEADLINES)


def debug_page_elements(driver, page_name=""):
    """Debug function to log all available input fields and their attributes"""
    try:
        log_msg(f"\n===== DEBUG: Page Elements on {page_name} =====")
        
        # Get all input fields
        inputs = driver.find_elements(By.TAG_NAME, "input")
        log_msg(f"Found {len(inputs)} input fields:")
        for idx, inp in enumerate(inputs):
            try:
                inp_id = inp.get_attribute("id") or "N/A"
                inp_name = inp.get_attribute("name") or "N/A"
                inp_type = inp.get_attribute("type") or "N/A"
                inp_placeholder = inp.get_attribute("placeholder") or "N/A"
                inp_value = inp.get_attribute("value") or "N/A"
                inp_class = inp.get_attribute("class") or "N/A"
                log_msg(f"  [{idx}] ID: {inp_id} | Name: {inp_name} | Type: {inp_type} | Placeholder: {inp_placeholder} | Class: {inp_class}")
            except:
                pass
        
        # Get all textarea fields
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        log_msg(f"Found {len(textareas)} textarea fields:")
        for idx, ta in enumerate(textareas):
            try:
                ta_id = ta.get_attribute("id") or "N/A"
                ta_name = ta.get_attribute("name") or "N/A"
                ta_placeholder = ta.get_attribute("placeholder") or "N/A"
                ta_class = ta.get_attribute("class") or "N/A"
                log_msg(f"  [{idx}] ID: {ta_id} | Name: {ta_name} | Placeholder: {ta_placeholder} | Class: {ta_class}")
            except:
                pass
        
        # Get all buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        log_msg(f"Found {len(buttons)} button fields:")
        for idx, btn in enumerate(buttons[:20]):
            try:
                btn_id = btn.get_attribute("id") or "N/A"
                btn_text = btn.text or "N/A"
                btn_type = btn.get_attribute("type") or "N/A"
                btn_class = btn.get_attribute("class") or "N/A"
                log_msg(f"  [{idx}] ID: {btn_id} | Text: {btn_text[:30]} | Type: {btn_type} | Class: {btn_class[:50]}")
            except:
                pass
        
        log_msg(f"===== END DEBUG =====\n")
    except Exception as e:
        log_msg(f"Error in debug_page_elements: {e}")


def randomText():
    return "".join(choice(ascii_uppercase + digits) for _ in range(randint(1, 5)))


def Logout(driver):
    """Logout from Naukri session"""
    try:
        drawer_xpaths = [
            f"//*[contains({ci('@class')}, 'drawer__icon')]",
            f"//div[contains({ci('@class')}, 'drawer')]"
        ]

        for xpath in drawer_xpaths:
            if is_element_present(driver, By.XPATH, xpath):
                try:
                    el = GetElement(driver, xpath, locator="XPATH")
                    if el:
                        el.click()
                        time.sleep(1)
                        log_msg("Drawer menu opened")
                        break
                except Exception as e:
                    log_msg(f"Drawer open failed ({xpath}): {e}")
                    continue

        logout_xpaths = [
            "//a[@data-type='logoutLink']",
            f"//a[contains({ci('@class')}, 'list-cta') and contains({ci('@title')}, 'logout')]",
            f"//a[contains({ci('@class')}, 'logout')]",
            f"//a[contains({ci('@href')}, 'logout')]",
            f"//*[contains({ci('text()')}, 'logout')]",
            f"//*[contains({ci('.')}, 'logout')]",
        ]

        for xpath in logout_xpaths:
            if is_element_present(driver, By.XPATH, xpath):
                try:
                    el = GetElement(driver, xpath, locator="XPATH")
                    if el:
                        driver.execute_script("arguments[0].scrollIntoView(true);", el)
                        time.sleep(0.5)
                        el.click()
                        time.sleep(2)
                        log_msg("Logout Successful")
                        return True
                except Exception as e:
                    log_msg(f"Logout click failed ({xpath}): {e}")
                    continue

        log_msg("Logout button not found")
        return False

    except Exception as e:
        log_msg(f"Logout error: {e}")
        return False


def LoadNaukri(headless):
    """Open Chrome to load Naukri.com"""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popups")
    options.add_argument("--disable-gpu")
    if headless:
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("headless")

    driver = None
    try:
        driver = webdriver.Chrome(options=options, service=ChromeService())
    except Exception as e:
        print(f"Error launching Chrome: {e}")
        driver = webdriver.Chrome(options)
    log_msg("Google Chrome Launched!")

    driver.implicitly_wait(5)
    driver.get(NAUKRI_LOGIN_URL)
    return driver


def naukriLogin(headless=False):
    """Open Chrome browser and Login to Naukri.com"""
    status = False
    driver = None
    username_locator = "usernameField"
    password_locator = "passwordField"
    login_btn_locator = "//*[@type='submit' and normalize-space()='Login']"
    skip_locator = "//*[text() = 'SKIP AND CONTINUE']"
    close_locator = "//*[contains(@class, 'cross-icon') or @alt='cross-icon']"

    try:
        driver = LoadNaukri(headless)

        log_msg(driver.title)
        if "naukri.com" in driver.title.lower():
            log_msg("Website Loaded Successfully.")

        emailFieldElement = None
        if is_element_present(driver, By.ID, username_locator):
            emailFieldElement = GetElement(driver, username_locator, locator="ID")
            time.sleep(1)
            passFieldElement = GetElement(driver, password_locator, locator="ID")
            time.sleep(1)
            loginButton = GetElement(driver, login_btn_locator, locator="XPATH")
        else:
            log_msg("None of the elements found to login.")

        if emailFieldElement is not None:
            emailFieldElement.clear()
            emailFieldElement.send_keys(username)
            time.sleep(1)
            passFieldElement.clear()
            passFieldElement.send_keys(password)
            time.sleep(1)
            loginButton.send_keys(Keys.ENTER)
            time.sleep(3)

            print("Checking Skip button")
            if WaitTillElementPresent(driver, close_locator, "XPATH", 10):
                GetElement(driver, close_locator, "XPATH").click()
            if WaitTillElementPresent(driver, skip_locator, "XPATH", 5):
                GetElement(driver, skip_locator, "XPATH").click()

            if WaitTillElementPresent(driver, "ff-inventory", locator="ID", timeout=40):
                CheckPoint = GetElement(driver, "ff-inventory", locator="ID")
                if CheckPoint:
                    log_msg("Naukri Login Successful")
                    status = True
                    return (status, driver)
                else:
                    log_msg("Unknown Login Error")
                    return (status, driver)
            else:
                log_msg("Unknown Login Error")
                return (status, driver)

    except Exception as e:
        catch(e)
    return (status, driver)


def UpdateProfile(driver):
    """Update user profile with mobile number and headline"""
    try:
        log_msg("Starting Profile Update...")
        
        view_profile_xpaths = [
            "//*[contains(@class, 'view-profile')]//a",
            "//a[contains(@class, 'view-profile')]",
            "//*[text()='View Profile']",
            "//button[contains(@class, 'profile')]",
        ]
        
        profile_clicked = False
        for xpath in view_profile_xpaths:
            try:
                if is_element_present(driver, By.XPATH, xpath):
                    log_msg(f"Found view profile link: {xpath}")
                    profElement = GetElement(driver, xpath, locator="XPATH")
                    if profElement:
                        profElement.click()
                        time.sleep(2)
                        profile_clicked = True
                        log_msg("Clicked view profile")
                        break
            except Exception as e:
                log_msg(f"Failed to click view profile {xpath}: {e}")
                continue
        
        if not profile_clicked:
            log_msg("Could not find view profile link")
            return

        close_locators = [
            "//*[contains(@class, 'crossIcon')]",
            "//*[contains(@class, 'cross-icon')]",
            "//button[contains(@class, 'close')]",
        ]
        
        for close_loc in close_locators:
            try:
                if is_element_present(driver, By.XPATH, close_loc):
                    GetElement(driver, close_loc, locator="XPATH").click()
                    time.sleep(2)
                    log_msg("Closed popup")
                    break
            except:
                pass

        # DEBUG: Log all page elements
        debug_page_elements(driver, "Profile Page - Initial")
        
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        
        debug_page_elements(driver, "Profile Page - After Scroll")

        # Try to update headline
        headline_xpaths = [
            "//input[@name='headline']",
            "//input[@id='headline']",
            "//*[@placeholder='Enter your professional headline']",
            "//input[contains(@placeholder, 'headline')]",
            "//textarea[@name='headline']",
        ]
        
        headline_updated = False
        for xpath in headline_xpaths:
            try:
                if is_element_present(driver, By.XPATH, xpath):
                    log_msg(f"Found headline field: {xpath}")
                    headlineElement = GetElement(driver, xpath, locator="XPATH")
                    if headlineElement:
                        current_headline = headlineElement.get_attribute("value")
                        if not current_headline:
                            current_headline = headlineElement.text
                        new_headline = get_random_headline()
                        if current_headline != new_headline:
                            headlineElement.clear()
                            headlineElement.send_keys(new_headline)
                            time.sleep(1)
                            log_msg(f"Updated headline to: {new_headline}")
                            headline_updated = True
                        else:
                            log_msg(f"Headline already current: {new_headline}")
                        break
            except Exception as e:
                log_msg(f"Failed to update headline {xpath}: {e}")
                continue
        
        if headline_updated:
            log_msg(f"Headline successfully updated")
        else:
            log_msg("Note: Headline field may not be on this page. It might be in a separate 'Edit Professional Headline' section. Check your profile page manually to locate it.")
            log_msg("You can create a separate Naukri API or use the UI inspector to identify the exact field name.")

        # Try to find edit button
        edit_xpaths = [
            "(//*[contains(@class, 'icon edit')])[1]",
            "//*[contains(@class, 'edit')]",
            "//button[contains(text(), 'Edit')]",
            "//*[@aria-label='Edit']",
        ]
        
        edit_clicked = False
        for xpath in edit_xpaths:
            try:
                if is_element_present(driver, By.XPATH, xpath):
                    log_msg(f"Found edit button: {xpath}")
                    editElement = GetElement(driver, xpath, locator="XPATH")
                    if editElement:
                        driver.execute_script("arguments[0].scrollIntoView(true);", editElement)
                        time.sleep(1)
                        try:
                            editElement.click()
                        except:
                            driver.execute_script("arguments[0].click();", editElement)
                        time.sleep(2)
                        edit_clicked = True
                        log_msg("Clicked edit button")
                        break
            except Exception as e:
                log_msg(f"Failed to click edit {xpath}: {e}")
                continue
        
        if edit_clicked:
            time.sleep(2)
            debug_page_elements(driver, "Profile Page - After Edit Click")
        
        if not edit_clicked:
            log_msg("Could not find edit button")
            return

        mobile_xpaths = [
            "//*[@name='mobile']",
            "//*[@id='mob_number']",
            "//input[contains(@name, 'mobile')]",
            "//input[contains(@id, 'mobile')]",
            "//input[contains(@placeholder, 'mobile')]",
        ]
        
        mobile_updated = False
        for xpath in mobile_xpaths:
            try:
                if is_element_present(driver, By.XPATH, xpath):
                    log_msg(f"Found mobile field: {xpath}")
                    mobFieldElement = GetElement(driver, xpath, locator="XPATH")
                    if mobFieldElement:
                        mobFieldElement.clear()
                        mobFieldElement.send_keys(mob)
                        time.sleep(1)
                        mobile_updated = True
                        log_msg(f"Updated mobile number: {mob}")
                        break
            except Exception as e:
                log_msg(f"Failed to update mobile {xpath}: {e}")
                continue
        
        if not mobile_updated:
            log_msg("Could not find mobile field to update")

        save_xpaths = [
            "//button[@type='submit'][@value='Save Changes']",
            "//*[@id='saveBasicDetailsBtn']",
            "//button[contains(text(), 'Save')]",
            "//button[contains(@class, 'save')]",
        ]
        
        save_clicked = False
        for save_xpath in save_xpaths:
            try:
                if is_element_present(driver, By.XPATH, save_xpath):
                    log_msg(f"Found save button: {save_xpath}")
                    saveElement = GetElement(driver, save_xpath, locator="XPATH")
                    if saveElement:
                        driver.execute_script("arguments[0].scrollIntoView(true);", saveElement)
                        time.sleep(1)
                        try:
                            saveElement.click()
                        except:
                            driver.execute_script("arguments[0].click();", saveElement)
                        log_msg("Clicked save button")
                        time.sleep(3)
                        save_clicked = True
                        break
            except Exception as e:
                log_msg(f"Failed to click save button {save_xpath}: {e}")
                continue
        
        if not save_clicked:
            log_msg("Could not find save button")
            return

        confirm_xpaths = [
            "//*[text() = 'today' or text()='Today']",
            "//*[contains(text(), 'saved')]",
            "//*[contains(@class, 'confirmMessage')]",
            "//*[@id='confirmMessage']",
        ]
        
        for xpath in confirm_xpaths:
            try:
                if is_element_present(driver, By.XPATH, xpath):
                    log_msg("Profile update confirmed")
                    break
            except:
                pass

        log_msg("Profile Update Completed")
        time.sleep(5)

    except Exception as e:
        log_msg(f"Error in UpdateProfile: {e}")
        catch(e)


def UpdateResume():
    """Update resume with random hidden text"""
    try:
        txt = randomText()
        xloc = randint(700, 1000)
        fsize = randint(1, 10)

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", fsize)
        can.drawString(xloc, 100, txt)
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)
        with open(originalResumePath, "rb") as f:
            existing_pdf = PdfReader(f)
            pagecount = len(existing_pdf.pages)
            print("Found %s pages in PDF" % pagecount)

            output = PdfWriter()
            for pageNum in range(pagecount - 1):
                output.add_page(existing_pdf.pages[pageNum])
            page = existing_pdf.pages[pagecount - 1]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

            with open(modifiedResumePath, "wb") as outputStream:
                output.write(outputStream)
            print("Saved modified PDF: %s" % modifiedResumePath)
            return os.path.abspath(modifiedResumePath)
    except Exception as e:
        catch(e)
    return os.path.abspath(originalResumePath)


def UploadResume(driver, resumePath):
    """Upload resume to Naukri profile"""
    try:
        log_msg("Starting Resume Upload...")
        driver.get(NAUKRI_PROFILE_URL)
        time.sleep(3)

        close_locators = [
            "//*[contains(@class, 'crossIcon')]",
            "//*[contains(@class, 'cross-icon')]",
            "//button[contains(@class, 'close')]",
            "//*[@aria-label='Close']"
        ]
        
        for close_loc in close_locators:
            try:
                if is_element_present(driver, By.XPATH, close_loc):
                    el = GetElement(driver, close_loc, locator="XPATH")
                    if el:
                        el.click()
                        time.sleep(1)
                        log_msg("Closed popup")
                        break
            except:
                pass

        file_input_xpaths = [
            "//input[@id='attachCV']",
            "//input[@id='lazyAttachCV']",
            "//input[@type='file' and contains(@id, 'attach')]",
            "//input[@type='file' and contains(@id, 'CV')]",
            "//input[@type='file' and contains(@class, 'upload')]",
            "//input[@type='file']",
        ]
        
        file_uploaded = False
        for xpath in file_input_xpaths:
            try:
                if is_element_present(driver, By.XPATH, xpath):
                    log_msg(f"Found file input: {xpath}")
                    AttachElement = GetElement(driver, xpath, locator="XPATH")
                    if AttachElement:
                        AttachElement.send_keys(os.path.abspath(resumePath))
                        log_msg(f"Resume sent to: {xpath}")
                        time.sleep(2)
                        file_uploaded = True
                        break
            except Exception as e:
                log_msg(f"Failed with xpath {xpath}: {e}")
                continue
        
        if not file_uploaded:
            log_msg("Could not find file input element. Trying alternative methods...")
        
        save_button_xpaths = [
            "//button[contains(text(), 'Save')]",
            "//button[contains(@class, 'save')]",
            "//button[@type='submit']",
            "//*[@id='saveBasicDetailsBtn']",
            "//button[contains(text(), 'Update')]",
            "//*[contains(@class, 'btn') and contains(text(), 'Save')]",
        ]
        
        save_clicked = False
        for save_xpath in save_button_xpaths:
            try:
                if is_element_present(driver, By.XPATH, save_xpath):
                    log_msg(f"Found save button: {save_xpath}")
                    saveElement = GetElement(driver, save_xpath, locator="XPATH")
                    if saveElement:
                        driver.execute_script("arguments[0].scrollIntoView(true);", saveElement)
                        time.sleep(1)
                        try:
                            saveElement.click()
                        except:
                            driver.execute_script("arguments[0].click();", saveElement)
                        log_msg("Clicked save button")
                        time.sleep(3)
                        save_clicked = True
                        break
            except Exception as e:
                log_msg(f"Failed to click save button {save_xpath}: {e}")
                continue
        
        if not save_clicked:
            log_msg("Could not find or click save button")

        success_xpaths = [
            "//*[contains(@class, 'updateOn')]",
            "//*[contains(text(), 'updated')]",
            "//*[contains(text(), 'Successfully')]",
            "//*[contains(text(), 'success')]",
        ]
        
        time.sleep(2)
        success_found = False
        for success_xpath in success_xpaths:
            try:
                if is_element_present(driver, By.XPATH, success_xpath):
                    CheckPoint = GetElement(driver, success_xpath, locator="XPATH")
                    if CheckPoint:
                        LastUpdatedDate = CheckPoint.text
                        log_msg(f"Success message found: {LastUpdatedDate}")
                        todaysDate1 = datetime.today().strftime("%b %d, %Y")
                        todaysDate2 = datetime.today().strftime("%b %#d, %Y")
                        if todaysDate1 in LastUpdatedDate or todaysDate2 in LastUpdatedDate:
                            log_msg("Resume Document Upload Successful. Last Updated date = %s" % LastUpdatedDate)
                        else:
                            log_msg("Resume Document Upload completed. Last Updated date = %s" % LastUpdatedDate)
                        success_found = True
                        break
            except:
                pass
        
        if not success_found:
            log_msg("Resume upload process completed (verification pending)")

    except Exception as e:
        log_msg(f"Error in UploadResume: {e}")
        catch(e)
    time.sleep(2)


def main():
    """Main execution function"""
    log_msg("-----Naukri.py Script Run Begin-----")
    driver = None
    try:
        status, driver = naukriLogin(headless)
        if status:
            if update_profile:
                UpdateProfile(driver)
            
            if upload_resume:
                if os.path.exists(originalResumePath):
                    if updatePDF:
                        resumePath = UpdateResume()
                        UploadResume(driver, resumePath)
                    else:
                        UploadResume(driver, originalResumePath)
                else:
                    log_msg("Resume not found at %s " % originalResumePath)

    except Exception as e:
        catch(e)

    finally:
        if driver is not None:
            try:
                Logout(driver)
                time.sleep(2)
            except Exception as e:
                log_msg("Error during logout: %s" % e)
        tearDown(driver)

    log_msg("-----Naukri.py Script Run Ended-----\n")


if __name__ == "__main__":
    main()
