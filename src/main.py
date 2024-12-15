"""Main entry point for the application."""
import sys
import signal
from rich.traceback import install
from .core.driver import DriverManager
from .core.tab_manager import TabManager
from .utils.logging import console, print_status, print_error
from .config.constants import MAX_RETRIES

def setup_signal_handlers(driver):
    """Setup signal handlers for graceful exit."""
    DriverManager.set_driver(driver)

    def signal_handler(signum, frame):
        print("\nReceived exit signal. Cleaning up...")
        current_driver = DriverManager.get_driver()
        if current_driver:
            DriverManager.cleanup_driver(current_driver)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def main():
    """Main function with enhanced error handling and cleanup."""
    install(show_locals=False, suppress=[])
    console.clear()
    
    driver = None
    try:
        driver = DriverManager.create_driver()
        if not driver:
            raise Exception("Failed to create driver")
            
        setup_signal_handlers(driver)
        handle_login(driver, auto_retry=True)
        
        while handle_processing_cycle(driver):
            pass
            
    except KeyboardInterrupt:
        console.print("\nGracefully shutting down...", style="warning")
    except Exception as e:
        print_error(e, "Fatal error")
    finally:
        if driver:
            with console.status("Cleaning up..."):
                DriverManager.cleanup_driver(driver)
        console.print("\n✨ Script ended", style="info")
        sys.exit(0)

if __name__ == "__main__":
    main()