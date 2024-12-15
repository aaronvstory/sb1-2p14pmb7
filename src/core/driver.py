"""Chrome driver management functionality."""
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from ..utils.logging import print_status
from ..config.constants import MAX_RETRIES

class DriverManager:
    _instance = None

    def __init__(self, driver: Optional[uc.Chrome] = None):
        self.driver = driver

    @classmethod
    def set_driver(cls, driver: uc.Chrome):
        if not cls._instance:
            cls._instance = cls(driver)
        else:
            cls._instance.driver = driver

    @classmethod
    def get_driver(cls):
        return cls._instance.driver if cls._instance else None

    @staticmethod
    def create_driver() -> uc.Chrome:
        """Create an undetectable Chrome driver with improved reliability."""
        for attempt in range(MAX_RETRIES):
            try:
                options = uc.ChromeOptions()
                options.binary_location = (
                    "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
                )
                
                # Core stability options
                stability_options = [
                    "--no-sandbox",
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    "--disable-software-rasterizer",
                    "--disable-features=VizDisplayCompositor",
                    "--disable-notifications",
                    "--disable-infobars",
                    "--mute-audio"
                ]
                for option in stability_options:
                    options.add_argument(option)

                # Mobile user agent
                mobile_ua = "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36"
                options.add_argument(f"--user-agent={mobile_ua}")
                options.add_argument("--window-size=560,840")

                # Browser preferences
                prefs = {
                    "intl.accept_languages": "en,en_US",
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False
                }
                options.add_experimental_option("prefs", prefs)

                driver = uc.Chrome(options=options)
                driver.set_page_load_timeout(30)
                driver.set_window_size(560, 840)
                
                return driver

            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    raise RuntimeError(f"Failed to create driver after {MAX_RETRIES} attempts: {str(e)}")
                print_status(f"Attempt {attempt + 1} failed, retrying...", "warning")
                time.sleep(2)

    @staticmethod
    def cleanup_driver(driver: uc.Chrome) -> None:
        """Clean up browser resources."""
        if not driver:
            return
        try:
            handles = driver.window_handles
            for handle in handles[1:]:
                try:
                    driver.switch_to.window(handle)
                    driver.close()
                except Exception as e:
                    logging.error(f"Error closing window: {e}")
            if handles:
                driver.switch_to.window(handles[0])
        except Exception as e:
            logging.error(f"Error in cleanup: {e}")
        finally:
            try:
                driver.quit()
            except:
                pass