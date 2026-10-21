import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:5173",
        help="Base URL for the frontend application (default: http://localhost:5173)"
    )
    parser.addoption(
        "--api-url",
        action="store",
        default="http://localhost:8000",
        help="Base URL for the backend API (default: http://localhost:8000)"
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in visible (headed) mode (default is headless)"
    )

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")

@pytest.fixture(scope="session")
def api_url(request):
    return request.config.getoption("--api-url").rstrip("/")

@pytest.fixture(scope="function")
def driver(request):
    """Initializes a clean Chrome WebDriver instance for each test."""
    options = Options()
    is_headed = request.config.getoption("--headed")
    
    if not is_headed:
        options.add_argument("--headless=new")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Enable browser console logging
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(4)
    
    yield driver
    
    try:
        driver.quit()
    except Exception:
        pass

@pytest.fixture(scope="function")
def logged_in_driver(driver, base_url):
    """Provides a driver pre-authenticated as standard user, navigated to /dashboard."""
    driver.get(f"{base_url}/login")
    WebDriverWait(driver, 6).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    
    driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys("user@circulareconomy.org")
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("Password123!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    WebDriverWait(driver, 6).until(
        EC.url_contains("/dashboard")
    )
    return driver

@pytest.fixture(scope="function")
def admin_driver(driver, base_url):
    """Provides a driver pre-authenticated as admin user, navigated to /admin-dashboard."""
    driver.get(f"{base_url}/login")
    WebDriverWait(driver, 6).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    
    driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys("admin_test@circulareconomy.org")
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("AdminPass123!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    WebDriverWait(driver, 6).until(
        EC.url_contains("/admin-dashboard")
    )
    return driver

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures screenshot on failure and attaches to HTML report."""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver") or item.funcargs.get("admin_driver")
        if driver:
            screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            try:
                driver.save_screenshot(screenshot_path)
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    extras.append(pytest_html.extras.image(screenshot_path))
            except Exception as e:
                print(f"Failed to save screenshot: {e}")
        report.extras = extras
