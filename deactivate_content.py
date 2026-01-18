#!/usr/bin/env python3
"""
Amazon Kids Plus Content Deactivator

This script automates the process of deactivating all content on the Amazon Kids
parent dashboard using Selenium WebDriver.

IMPORTANT: This script contains placeholder CSS selectors and button text that may
need to be customized based on Amazon's current website structure. Before using,
inspect the actual Amazon Kids dashboard and update the selectors as needed.
"""

import os
import time
import logging
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AmazonKidsContentDeactivator:
    """Handles automation of content deactivation on Amazon Kids dashboard."""
    
    def __init__(self):
        """Initialize the deactivator with configuration from environment variables."""
        load_dotenv()
        
        self.email = os.getenv('AMAZON_EMAIL')
        self.password = os.getenv('AMAZON_PASSWORD')
        self.page_load_timeout = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
        self.element_wait_timeout = int(os.getenv('ELEMENT_WAIT_TIMEOUT', '10'))
        self.headless = os.getenv('HEADLESS', 'false').lower() == 'true'
        self.max_iterations = int(os.getenv('MAX_ITERATIONS', '100'))
        
        # Customizable selectors - update these based on actual Amazon page structure
        self.checkbox_selector = os.getenv('CHECKBOX_SELECTOR', 'input[type="checkbox"]:checked')
        self.content_link_text = os.getenv('CONTENT_LINK_TEXT', 'Manage Content')
        
        if not self.email or not self.password:
            raise ValueError("AMAZON_EMAIL and AMAZON_PASSWORD must be set in .env file")
        
        self.driver = None
        self.wait = None
        self.unchecked_count = 0
        
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        logger.info("Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(self.page_load_timeout)
        self.driver.maximize_window()
        
        self.wait = WebDriverWait(self.driver, self.element_wait_timeout)
        logger.info("WebDriver setup complete")
        
    def login(self):
        """Log in to Amazon account."""
        logger.info("Navigating to Amazon Kids parent dashboard...")
        
        # Navigate to Amazon Kids+ parent dashboard
        self.driver.get('https://www.amazon.com/freeTime/home')
        time.sleep(2)
        
        try:
            # Check if we need to log in
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, 'ap_email'))
            )
            logger.info("Login page detected, entering credentials...")
            
            # Enter email
            email_field.clear()
            email_field.send_keys(self.email)
            
            # Click continue button
            continue_btn = self.driver.find_element(By.ID, 'continue')
            continue_btn.click()
            time.sleep(1)
            
            # Enter password
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, 'ap_password'))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            
            # Click sign in button
            signin_btn = self.driver.find_element(By.ID, 'signInSubmit')
            signin_btn.click()
            
            logger.info("Login submitted, waiting for dashboard...")
            time.sleep(3)
            
        except TimeoutException:
            logger.info("Already logged in or login page not found")
            
    def navigate_to_content_management(self):
        """Navigate to the content management page where items can be unchecked."""
        logger.info("Navigating to content management page...")
        
        # NOTE: This navigation logic is a placeholder and may need customization
        # based on the actual Amazon Kids dashboard structure.
        # 
        # To customize:
        # 1. Manually navigate to the content management page
        # 2. Use browser DevTools to inspect the navigation elements
        # 3. Update the selector or use direct URL navigation
        
        try:
            # Try to find and click on content management link using configured text
            content_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, self.content_link_text))
            )
            content_link.click()
            time.sleep(2)
        except TimeoutException:
            logger.warning(f"Could not find '{self.content_link_text}' link")
            logger.warning("You may need to:")
            logger.warning("1. Navigate manually to the content page, or")
            logger.warning("2. Update CONTENT_LINK_TEXT in .env, or")
            logger.warning("3. Modify the navigation logic in the script")
            # The script will continue and try to work with whatever page is loaded
            
    def uncheck_all_visible_content(self) -> int:
        """
        Uncheck all currently visible checked checkboxes.
        
        NOTE: The checkbox selector is configurable via CHECKBOX_SELECTOR environment
        variable. The default 'input[type="checkbox"]:checked' may need to be updated
        based on Amazon's actual page structure.
        
        Returns:
            int: Number of checkboxes unchecked in this iteration
        """
        unchecked_in_iteration = 0
        
        try:
            # Find all checked checkboxes using configured selector
            checked_boxes = self.driver.find_elements(
                By.CSS_SELECTOR, 
                self.checkbox_selector
            )
            
            logger.info(f"Found {len(checked_boxes)} checked items")
            
            if len(checked_boxes) == 0:
                logger.warning(f"No checkboxes found with selector: {self.checkbox_selector}")
                logger.warning("You may need to update CHECKBOX_SELECTOR in .env")
                logger.warning("Use browser DevTools to inspect the checkbox elements")
            
            for checkbox in checked_boxes:
                try:
                    # Scroll element into view
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                        checkbox
                    )
                    time.sleep(0.3)
                    
                    # Check if still checked (in case of dynamic page updates)
                    if checkbox.is_selected():
                        # Try to click using JavaScript if regular click fails
                        try:
                            checkbox.click()
                        except ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", checkbox)
                        
                        unchecked_in_iteration += 1
                        self.unchecked_count += 1
                        logger.info(f"Unchecked item {self.unchecked_count}")
                        time.sleep(0.2)  # Small delay to avoid overwhelming the page
                        
                except StaleElementReferenceException:
                    logger.warning("Element became stale, skipping...")
                    continue
                except Exception as e:
                    logger.error(f"Error unchecking item: {e}")
                    continue
                    
        except NoSuchElementException:
            logger.info("No checked items found")
            
        return unchecked_in_iteration
        
    def scroll_to_bottom(self):
        """Scroll to the bottom of the page to trigger lazy loading."""
        logger.info("Scrolling to bottom of page...")
        
        # Get current scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        # Scroll down
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        
        return new_height != last_height
        
    def click_load_more_button(self) -> bool:
        """
        Click the 'Load More' or 'Show More' button if it exists.
        
        NOTE: Button selectors are configurable but default to common patterns.
        If the script doesn't find the button, inspect Amazon's page and update
        the selectors in this method.
        
        Returns:
            bool: True if button was clicked, False otherwise
        """
        try:
            # Common button texts and selectors
            # These are generic patterns - may need customization for Amazon's specific implementation
            button_selectors = [
                (By.XPATH, "//button[contains(text(), 'Load More')]"),
                (By.XPATH, "//button[contains(text(), 'Show More')]"),
                (By.XPATH, "//button[contains(text(), 'More Results')]"),
                (By.XPATH, "//a[contains(text(), 'Load More')]"),
                (By.CSS_SELECTOR, "button.load-more"),
                (By.CSS_SELECTOR, "button.show-more"),
                (By.CSS_SELECTOR, "a.load-more"),
                # Add more selectors here based on actual Amazon implementation
            ]
            
            for by, selector in button_selectors:
                try:
                    button = self.driver.find_element(by, selector)
                    if button.is_displayed() and button.is_enabled():
                        logger.info(f"Found 'Load More' button, clicking...")
                        
                        # Scroll to button
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                            button
                        )
                        time.sleep(1)
                        
                        # Click button
                        try:
                            button.click()
                        except ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", button)
                        
                        time.sleep(2)  # Wait for content to load
                        return True
                        
                except NoSuchElementException:
                    continue
                    
            logger.info("No 'Load More' button found")
            return False
            
        except Exception as e:
            logger.error(f"Error clicking load more button: {e}")
            return False
            
    def deactivate_all_content(self):
        """Main method to deactivate all content on the dashboard."""
        logger.info("Starting content deactivation process...")
        
        # Use configured max iterations (default 100, configurable via MAX_ITERATIONS env var)
        max_iterations = self.max_iterations
        iteration = 0
        consecutive_no_changes = 0
        
        logger.info(f"Maximum iterations set to: {max_iterations}")
        logger.info(f"Using checkbox selector: {self.checkbox_selector}")
        
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"\n--- Iteration {iteration} ---")
            
            # Uncheck all visible content
            unchecked = self.uncheck_all_visible_content()
            
            if unchecked == 0:
                consecutive_no_changes += 1
                logger.info("No items unchecked in this iteration")
            else:
                consecutive_no_changes = 0
                
            # If no changes for 2 consecutive iterations, we're likely done
            if consecutive_no_changes >= 2:
                logger.info("No changes for 2 consecutive iterations, assuming complete")
                break
                
            # Try to scroll down
            scroll_changed = self.scroll_to_bottom()
            
            # Try to click load more button
            button_clicked = self.click_load_more_button()
            
            # If neither scrolling revealed new content nor button was clicked, we're done
            if not scroll_changed and not button_clicked and consecutive_no_changes > 0:
                logger.info("No more content to load")
                break
                
            time.sleep(1)
            
        logger.info(f"\nDeactivation complete! Total items unchecked: {self.unchecked_count}")
        
    def run(self):
        """Execute the complete automation workflow."""
        try:
            self.setup_driver()
            self.login()
            self.navigate_to_content_management()
            self.deactivate_all_content()
            
            logger.info("\n=== Automation completed successfully ===")
            logger.info(f"Total content items deactivated: {self.unchecked_count}")
            
            # Keep browser open for a few seconds so user can see the result
            if not self.headless:
                logger.info("Keeping browser open for 5 seconds...")
                time.sleep(5)
                
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
            raise
            
        finally:
            if self.driver:
                logger.info("Closing browser...")
                self.driver.quit()


def main():
    """Main entry point for the script."""
    try:
        deactivator = AmazonKidsContentDeactivator()
        deactivator.run()
    except KeyboardInterrupt:
        logger.info("\nScript interrupted by user")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
