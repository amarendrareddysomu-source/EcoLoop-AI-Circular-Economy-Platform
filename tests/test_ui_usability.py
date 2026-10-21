import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestScenario4UIUsabilityAndCompatibility:
    """SCENARIO 4: UI Usability, Visual Layout, and Responsive Compatibility Tests."""

    def test_tc_usab01_verify_important_page_headings(self, driver, base_url):
        """TC-USAB01: Verify that primary page headings (h1/h2) are clearly visible on login and register."""
        driver.get(f"{base_url}/login")
        heading = driver.find_element(By.TAG_NAME, "h2")
        assert heading.is_displayed()
        assert "Welcome Back" in heading.text

        driver.get(f"{base_url}/register")
        reg_heading = driver.find_element(By.TAG_NAME, "h2")
        assert reg_heading.is_displayed()
        assert "Create Account" in reg_heading.text

    def test_tc_usab02_verify_navigation_links_work(self, driver, base_url):
        """TC-USAB02: Verify that contextual anchor navigation links switch routes smoothly."""
        driver.get(f"{base_url}/login")
        register_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Register here')]")
        register_link.click()
        WebDriverWait(driver, 5).until(EC.url_contains("/register"))
        assert "/register" in driver.current_url

    def test_tc_usab03_verify_buttons_visible_and_enabled(self, driver, base_url):
        """TC-USAB03: Verify primary action buttons are visible, have readable dimensions, and are clickable."""
        driver.get(f"{base_url}/login")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert submit_btn.is_displayed()
        assert submit_btn.is_enabled()
        rect = submit_btn.rect
        assert rect["height"] >= 35
        assert rect["width"] >= 150

    def test_tc_usab04_verify_forms_expose_required_fields(self, driver, base_url):
        """TC-USAB04: Verify that registration and login forms properly expose HTML5 required attributes."""
        driver.get(f"{base_url}/register")
        email_input = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        assert email_input.get_attribute("required") is not None
        assert password_input.get_attribute("required") is not None

    def test_tc_usab05_verify_validation_messages_appear(self, driver, base_url):
        """TC-USAB05: Verify that validation alert notifications appear prominently with accessible styling."""
        driver.get(f"{base_url}/login")
        driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys("user@circulareconomy.org")
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("WrongPass123!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        WebDriverWait(driver, 6).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".bg-rose-950\\/60, [class*='text-rose-300']"))
        )
        alert = driver.find_element(By.CSS_SELECTOR, ".bg-rose-950\\/60, [class*='text-rose-300']")
        assert alert.is_displayed()
        assert "email or password" in alert.text.lower()

    def test_tc_usab06_check_for_broken_images(self, logged_in_driver, base_url):
        """TC-USAB06: Check that all rendered <img> tags have naturalWidth > 0 (no broken images)."""
        logged_in_driver.get(f"{base_url}/dashboard")
        images = logged_in_driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            # Check naturalWidth via JavaScript
            is_valid = logged_in_driver.execute_script(
                "return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0",
                img
            )
            assert is_valid, f"Broken image detected: {img.get_attribute('src')}"

    def test_tc_usab07_verify_page_navigation_without_console_errors(self, driver, base_url):
        """TC-USAB07: Ensure that navigating between pages produces zero uncaught React or runtime exceptions."""
        driver.get(f"{base_url}/login")
        driver.get(f"{base_url}/register")
        driver.get(f"{base_url}/forgot-password")
        
        logs = driver.get_log("browser")
        uncaught_errors = [e for e in logs if e.get("level") == "SEVERE" and "Uncaught" in e.get("message", "")]
        assert len(uncaught_errors) == 0, f"Uncaught exceptions detected: {uncaught_errors}"

    def test_tc_usab08_desktop_viewport_layout_check(self, driver, base_url):
        """TC-USAB08: Verify main interface fits standard desktop viewport (1920x1080) without horizontal scroll."""
        driver.set_window_size(1920, 1080)
        driver.get(f"{base_url}/login")
        scroll_width = driver.execute_script("return document.documentElement.scrollWidth;")
        client_width = driver.execute_script("return document.documentElement.clientWidth;")
        assert scroll_width <= client_width + 5, "Horizontal scrollbar appeared on desktop"

    def test_tc_usab09_tablet_viewport_compatibility(self, driver, base_url):
        """TC-USAB09: Verify tablet viewport (768x1024) layout adapts properly and keeps controls accessible."""
        driver.set_window_size(768, 1024)
        driver.get(f"{base_url}/login")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert submit_btn.is_displayed()
        card = driver.find_element(By.CSS_SELECTOR, ".glass-card, [class*='glass-card'], [class*='rounded-3xl']")
        assert card.is_displayed()

    def test_tc_usab10_mobile_viewport_compatibility(self, driver, base_url):
        """TC-USAB10: Verify mobile viewport (375x667) adapts cleanly without card clipping."""
        driver.set_window_size(375, 667)
        driver.get(f"{base_url}/login")
        scroll_width = driver.execute_script("return document.documentElement.scrollWidth;")
        client_width = driver.execute_script("return document.documentElement.clientWidth;")
        assert scroll_width <= client_width + 10, "Horizontal overflow detected on mobile viewport"
        assert driver.find_element(By.CSS_SELECTOR, "button[type='submit']").is_displayed()
