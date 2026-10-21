import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:5173",
        help="Base URL for the frontend application (default: http://localhost:5173)"
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in visible mode (default is headless)"
    )

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")

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
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    
    yield driver
    
    # Teardown
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failures and attach to pytest-html report."""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
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
                print(f"Failed to capture screenshot: {e}")
        report.extras = extras
