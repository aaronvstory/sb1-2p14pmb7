"""Tab management functionality."""
from typing import List
import time
from ..utils.logging import print_status

class TabManager:
    def __init__(self, driver: uc.Chrome):
        self.driver = driver
        self.active_tabs = {}  # {order_id: Order}
        self.tab_open_times = {}  # {handle: timestamp}
        self.original_handle = driver.current_window_handle
        self.processed_tabs = set()
        self.tabs_with_wait_times = {}

    def track_new_tab(self, handle: str, order_id: str):
        """Track a new tab's open time."""
        self.tab_open_times[handle] = time.time()
        self.active_tabs[order_id] = handle

    def get_oldest_tabs(self, count: int) -> List[str]:
        """Get handles of oldest tabs by open time."""
        sorted_tabs = sorted(self.tab_open_times.items(), key=lambda x: x[1])
        return [handle for handle, _ in sorted_tabs[:count]]

    def close_tabs(self, handles: List[str]) -> int:
        """Close specific tabs and return count of closed tabs."""
        closed = 0
        for handle in handles:
            try:
                if handle in self.driver.window_handles:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
                    closed += 1
                    self.tab_open_times.pop(handle, None)
            except Exception:
                continue
        return closed

    def quick_cleanup(self) -> None:
        """Rapidly close all tabs except main."""
        closed = 0
        for handle in self.driver.window_handles[1:]:
            try:
                self.driver.switch_to.window(handle)
                self.driver.close()
                closed += 1
            except:
                continue
        if closed > 0:
            print_status(f"Closed {closed} tabs", "info")
        self.restore_main_tab()

    def restore_main_tab(self):
        """Safely restore the main tab."""
        try:
            self.driver.switch_to.window(self.original_handle)
        except:
            if self.driver.window_handles:
                self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                self.driver.switch_to.new_window("tab")
                self.original_handle = self.driver.current_window_handle