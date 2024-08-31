import pytest
from selenium import webdriver
import os
import time

# Directory to save screenshots
SCREENSHOT_DIR = 'screenshots'


@pytest.fixture(scope="function")
def setup(request):
    driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.
    driver.get("https://www.saucedemo.com")
    driver.maximize_window()
    request.cls.driver = driver

    # Yield control back to the test
    yield driver

    # Quit the driver after the test
    driver.quit()


def pytest_runtest_makereport(item, call):
    # Check if the test failed
    if call.when == 'call' and call.excinfo is not None:
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)

        # Capture screenshot
        driver = item.funcargs['setup']
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot-{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
