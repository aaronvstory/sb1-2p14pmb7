"""Order management functionality."""
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils.logging import print_status
from ..config.constants import MAX_RETRIES

class Order:
    def __init__(self, element: uc.WebElement):
        """Initialize order from receipt link element."""
        try:
            self.receipt_url: str = None
            href = element.get_attribute("href")
            if href and "/orders/" in href:
                self.receipt_url = href
            else:
                link = element.find_element(By.CSS_SELECTOR, 'a[href*="/orders/"]')
                self.receipt_url = link.get_attribute("href")
                
            if not self.receipt_url:
                raise ValueError("No valid receipt URL found")
                
            self.id: str = (
                self.receipt_url.split("/orders/")[-1]
                .replace("/receipt/", "")
                .split("?")[0]
            ).strip()
            
            if not self.id:
                raise ValueError("Failed to extract order ID")
                
            self.short_id: str = self.id[-6:].upper()
            self.url: str = f"https://doordash.com/orders/{self.id}/help/"
            self.tab_handle: Optional[str] = None
            self.wait_time: Optional[int] = None
            
        except Exception as e:
            print_status(f"Error initializing order: {str(e)}", "error")
            raise ValueError(f"Failed to create order object: {str(e)}")

    def open_support_chat(self, driver: uc.Chrome) -> bool:
        """Open support chat with improved retry logic."""
        for retry in range(MAX_RETRIES):
            try:
                driver.get(self.url)
                wait = WebDriverWait(driver, 10)
                
                # Wait for page load
                time.sleep(1)
                
                # Click "It's something else"
                something_else = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//button[@aria-label="It\'s something else"]')
                    )
                )
                time.sleep(0.5)
                driver.execute_script("arguments[0].scrollIntoView(true);", something_else)
                driver.execute_script("arguments[0].click();", something_else)
                
                # Click "Contact support"
                contact = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(., 'Contact support')]")
                    )
                )
                time.sleep(0.5)
                driver.execute_script("arguments[0].scrollIntoView(true);", contact)
                driver.execute_script("arguments[0].click();", contact)
                
                time.sleep(2)
                return True
                
            except Exception:
                if retry == MAX_RETRIES - 1:
                    return False
                time.sleep(1)
                continue
        return False