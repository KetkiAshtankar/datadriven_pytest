# import pytest
# from selenium import webdriver
# import os
# import time

# # Directory to save screenshots
# SCREENSHOT_DIR = 'screenshots'


# @pytest.fixture(scope="function")
# def setup(request):
#     driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.
#     driver.get("https://www.saucedemo.com")
#     driver.maximize_window()
#     request.cls.driver = driver

#     # Yield control back to the test
#     yield driver

#     # Quit the driver after the test
#     driver.quit()


# def pytest_runtest_makereport(item, call):
#     # Check if the test failed
#     if call.when == 'call' and call.excinfo is not None:
#         # Create screenshots directory if it doesn't exist
#         if not os.path.exists(SCREENSHOT_DIR):
#             os.makedirs(SCREENSHOT_DIR)

#         # Capture screenshot
#         driver = item.funcargs['setup']
#         timestamp = time.strftime("%Y%m%d-%H%M%S")
#         screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot-{timestamp}.png")
#         driver.save_screenshot(screenshot_path)
#         print(f"Screenshot saved to {screenshot_path}")

import pytest
from selenium import webdriver
import os
import time
import allure

# Directory to save screenshots
SCREENSHOT_DIR = 'screenshots'

@pytest.fixture(scope="function")
def setup(request):
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com")
    driver.maximize_window()
    # If using a test class, make driver available as self.driver
    if hasattr(request, 'cls'):
        request.cls.driver = driver

    yield driver
    # Quit the driver after the test
    driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Let pytest run all other hooks to get the report object
    outcome = yield
    rep = outcome.get_result()

    # Only on the 'call' phase and when the test failed
    if rep.when == 'call' and rep.failed:
        try:
            # Ensure the screenshot directory exists
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)

            # Safely get the WebDriver instance from the 'setup' fixture
            driver = item.funcargs.get('setup')
            if driver:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"{item.name}-{timestamp}.png"
                screenshot_path = os.path.join(SCREENSHOT_DIR, filename)

                # Save screenshot to file
                success = driver.save_screenshot(screenshot_path)
                if success:
                    # Attach it to Allure
                    allure.attach.file(
                        screenshot_path,
                        name="Failure Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
                else:
                    print(f"[WARN] driver.save_screenshot returned False for {item.name}")
            else:
                print("[WARN] WebDriver fixture 'setup' not found; skipping screenshot.")
        except Exception as e:
            # Catch any errors during screenshot or attachment
            print(f"[ERROR] Exception during screenshot capture: {e}")

