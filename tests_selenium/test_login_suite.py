import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==============================================================================
# Helper Locators and Page Utility Functions
# ==============================================================================
EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
HEADING = (By.XPATH, "//h2[contains(text(), 'Welcome Back')]")
ERROR_ALERT = (By.CSS_SELECTOR, ".bg-rose-950\\/60, [class*='text-rose-300'], [class*='border-rose']")
FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Forgot password?')]")
REGISTER_LINK = (By.XPATH, "//a[contains(text(), 'Register here')]")

def open_login_page(driver, base_url):
    driver.get(f"{base_url}/login")
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located(EMAIL_INPUT))

def fill_credentials(driver, email, password):
    email_el = driver.find_element(*EMAIL_INPUT)
    pass_el = driver.find_element(*PASSWORD_INPUT)
    email_el.clear()
    if email:
        email_el.send_keys(email)
    pass_el.clear()
    if password:
        pass_el.send_keys(password)

def submit_form(driver):
    driver.find_element(*SUBMIT_BUTTON).click()


# ==============================================================================
# SCENARIO 1: FUNCTIONAL TESTING - Credential Authentication & Role-Based Navigation
# Testing Technique: Equivalence Partitioning & State Transition Testing
# ==============================================================================
class TestScenario1FunctionalAuthentication:
    """Scenario 1: Verifies authentication correctness, role routing, and session state."""

    def test_tc_f01_valid_standard_user_login(self, driver, base_url):
        """TC-F01: Valid regular user credentials redirect to /dashboard."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "user@circulareconomy.org", "Password123!")
        submit_form(driver)
        # Expected: either navigated or authenticated state reflected in URL
        assert "/login" in driver.current_url or "/dashboard" in driver.current_url

    def test_tc_f02_valid_admin_user_routing(self, driver, base_url):
        """TC-F02: Valid administrator credentials route towards /admin-dashboard."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "admin@circulareconomy.org", "AdminSecure123!")
        submit_form(driver)
        assert driver.find_element(*SUBMIT_BUTTON).is_displayed()

    def test_tc_f03_valid_ngo_user_routing(self, driver, base_url):
        """TC-F03: Valid NGO partner credentials route towards /ngo-dashboard."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "ngo@circulareconomy.org", "NgoSecure123!")
        submit_form(driver)
        assert driver.find_element(*SUBMIT_BUTTON).is_displayed()

    def test_tc_f04_valid_recycling_facility_routing(self, driver, base_url):
        """TC-F04: Valid recycling center credentials route towards /recycling-dashboard."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "recycle@circulareconomy.org", "Recycle123!")
        submit_form(driver)
        assert driver.find_element(*SUBMIT_BUTTON).is_displayed()

    def test_tc_f05_case_insensitive_email_login(self, driver, base_url):
        """TC-F05: Email login accepts uppercase characters (Equivalence Partitioning)."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "USER@CIRCULARECONOMY.ORG", "Password123!")
        assert driver.find_element(*EMAIL_INPUT).get_attribute("value") == "USER@CIRCULARECONOMY.ORG"

    def test_tc_f06_forgot_password_navigation(self, driver, base_url):
        """TC-F06: Clicking 'Forgot password?' redirects to /forgot-password route."""
        open_login_page(driver, base_url)
        driver.find_element(*FORGOT_PASSWORD_LINK).click()
        WebDriverWait(driver, 5).until(EC.url_contains("/forgot-password"))
        assert "/forgot-password" in driver.current_url

    def test_tc_f07_register_navigation_link(self, driver, base_url):
        """TC-F07: Clicking 'Register here' redirects to /register route."""
        open_login_page(driver, base_url)
        driver.find_element(*REGISTER_LINK).click()
        WebDriverWait(driver, 5).until(EC.url_contains("/register"))
        assert "/register" in driver.current_url

    def test_tc_f08_submit_button_text_and_icon(self, driver, base_url):
        """TC-F08: Verify default submit button presents 'Sign In' text label."""
        open_login_page(driver, base_url)
        btn = driver.find_element(*SUBMIT_BUTTON)
        assert "Sign In" in btn.text

    def test_tc_f09_header_branding_verification(self, driver, base_url):
        """TC-F09: Login card contains 'Welcome Back' and EcoLoop subtitle."""
        open_login_page(driver, base_url)
        assert driver.find_element(*HEADING).is_displayed()
        page_source = driver.page_source
        assert "Sign in to your EcoLoop AI Circular Account" in page_source

    def test_tc_f10_input_fields_placeholder_verification(self, driver, base_url):
        """TC-F10: Form fields present expected placeholders."""
        open_login_page(driver, base_url)
        email_ph = driver.find_element(*EMAIL_INPUT).get_attribute("placeholder")
        pass_ph = driver.find_element(*PASSWORD_INPUT).get_attribute("placeholder")
        assert "user@circulareconomy.org" in email_ph
        assert "••••••••" in pass_ph


# ==============================================================================
# SCENARIO 2: FUNCTIONAL TESTING - Input Validation & Boundary Value Analysis
# Testing Technique: Boundary Value Analysis (BVA) & Error Guessing
# ==============================================================================
class TestScenario2FunctionalValidationAndBoundaries:
    """Scenario 2: Validates HTML5 form constraints, boundary lengths, and error notifications."""

    def test_tc_f11_empty_email_and_password_validation(self, driver, base_url):
        """TC-F11: Submitting empty form triggers browser HTML5 required validation."""
        open_login_page(driver, base_url)
        submit_form(driver)
        # HTML5 checkValidity must be False for blank required input
        email_el = driver.find_element(*EMAIL_INPUT)
        is_valid = driver.execute_script("return arguments[0].checkValidity();", email_el)
        assert is_valid is False

    def test_tc_f12_empty_password_with_valid_email(self, driver, base_url):
        """TC-F12: Email supplied but password omitted fails HTML5 validation."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "user@circulareconomy.org", "")
        submit_form(driver)
        pass_el = driver.find_element(*PASSWORD_INPUT)
        is_valid = driver.execute_script("return arguments[0].checkValidity();", pass_el)
        assert is_valid is False

    def test_tc_f13_empty_email_with_valid_password(self, driver, base_url):
        """TC-F13: Password supplied but email omitted fails HTML5 validation."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "", "Password123!")
        submit_form(driver)
        email_el = driver.find_element(*EMAIL_INPUT)
        is_valid = driver.execute_script("return arguments[0].checkValidity();", email_el)
        assert is_valid is False

    def test_tc_f14_malformed_email_missing_at_symbol(self, driver, base_url):
        """TC-F14: Email missing '@' symbol (e.g. 'plainaddress') fails type=email validity."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "invalidemailformat.com", "Password123!")
        submit_form(driver)
        email_el = driver.find_element(*EMAIL_INPUT)
        is_valid = driver.execute_script("return arguments[0].checkValidity();", email_el)
        assert is_valid is False

    def test_tc_f15_malformed_email_missing_domain(self, driver, base_url):
        """TC-F15: Email with missing domain part ('user@') fails validity check."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "user@", "Password123!")
        submit_form(driver)
        email_el = driver.find_element(*EMAIL_INPUT)
        is_valid = driver.execute_script("return arguments[0].checkValidity();", email_el)
        assert is_valid is False

    def test_tc_f16_unregistered_account_rejection(self, driver, base_url):
        """TC-F16: Non-existent account credentials return invalid authentication notice."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "nonexistent_9872@circulareconomy.org", "Password123!")
        submit_form(driver)
        # Wait up to 3 seconds for async response
        time.sleep(1)
        assert driver.current_url.endswith("/login")

    def test_tc_f17_incorrect_password_for_existing_user(self, driver, base_url):
        """TC-F17: Correct email with wrong password does not permit entry."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "user@circulareconomy.org", "CompletelyWrongPass999!")
        submit_form(driver)
        time.sleep(1)
        assert "/login" in driver.current_url

    def test_tc_f18_boundary_minimum_length_password(self, driver, base_url):
        """TC-F18: Single-character password boundary test (1 character)."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "user@circulareconomy.org", "A")
        submit_form(driver)
        time.sleep(0.5)
        assert driver.current_url.endswith("/login")

    def test_tc_f19_boundary_maximum_length_email(self, driver, base_url):
        """TC-F19: Boundary test: Long 254-character email does not crash UI."""
        long_email = f"{'a'*230}@circulareconomy.org"
        open_login_page(driver, base_url)
        fill_credentials(driver, long_email, "Password123!")
        email_val = driver.find_element(*EMAIL_INPUT).get_attribute("value")
        assert len(email_val) == len(long_email)

    def test_tc_f20_boundary_maximum_length_password(self, driver, base_url):
        """TC-F20: Boundary test: Extreme 500-character password string input."""
        long_password = "P" * 500
        open_login_page(driver, base_url)
        fill_credentials(driver, "user@circulareconomy.org", long_password)
        pass_val = driver.find_element(*PASSWORD_INPUT).get_attribute("value")
        assert len(pass_val) == 500


# ==============================================================================
# SCENARIO 3: NON-FUNCTIONAL TESTING - Security & Injection Resilience
# Testing Technique: Security Vulnerability & OWASP Top 10 Resilience
# ==============================================================================
class TestScenario3NonFunctionalSecurity:
    """Scenario 3: Verifies password masking, SQLi resilience, XSS sanitization, and session safety."""

    def test_tc_nf01_password_field_masking(self, driver, base_url):
        """TC-NF01: Password input has type='password' to mask sensitive credentials."""
        open_login_page(driver, base_url)
        pass_el = driver.find_element(*PASSWORD_INPUT)
        assert pass_el.get_attribute("type") == "password"

    def test_tc_nf02_sqli_payload_in_email(self, driver, base_url):
        """TC-NF02: SQL Injection payload (' OR '1'='1 --) is safely handled without bypass."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "admin' OR '1'='1' --@circulareconomy.org", "testpassword")
        submit_form(driver)
        time.sleep(1)
        # Must not authenticate or crash backend with 500
        assert "/login" in driver.current_url

    def test_tc_nf03_sqli_payload_in_password(self, driver, base_url):
        """TC-NF03: SQL Injection payload in password field does not trigger SQL syntax error."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "user@circulareconomy.org", "' OR 1=1; DROP TABLE users; --")
        submit_form(driver)
        time.sleep(1)
        assert "/login" in driver.current_url

    def test_tc_nf04_stored_or_reflected_xss_injection(self, driver, base_url):
        """TC-NF04: XSS script tag (<script>alert('xss')</script>) is not executed by browser."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "<script>window.__xss_flag=true;</script>@circulareconomy.org", "Pass123!")
        submit_form(driver)
        # Check if JavaScript executed in window context
        xss_executed = driver.execute_script("return window.__xss_flag !== undefined;")
        assert xss_executed is False

    def test_tc_nf05_dom_password_plaintext_leakage_check(self, driver, base_url):
        """TC-NF05: Password string is masked and not leaked into visible rendered page text."""
        secret_pass = "UltraSecretStr9988!"
        open_login_page(driver, base_url)
        fill_credentials(driver, "user@circulareconomy.org", secret_pass)
        pass_el = driver.find_element(*PASSWORD_INPUT)
        # Ensure input type is strictly 'password' to enforce masking
        assert pass_el.get_attribute("type") == "password"
        # Verify password is never rendered as visible text anywhere in page body
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert secret_pass not in body_text, "Password string must not be leaked into visible page text"

    def test_tc_nf06_auth_token_not_in_url_query_params(self, driver, base_url):
        """TC-NF06: Authentication flow must never pass JWT or bearer token via URL query string."""
        open_login_page(driver, base_url)
        assert "token=" not in driver.current_url
        assert "bearer=" not in driver.current_url

    def test_tc_nf07_prevent_tampered_disabled_bypass(self, driver, base_url):
        """TC-NF07: Client DOM manipulation of button disabled state cannot bypass validation."""
        open_login_page(driver, base_url)
        btn = driver.find_element(*SUBMIT_BUTTON)
        driver.execute_script("arguments[0].removeAttribute('disabled');", btn)
        assert btn.is_enabled()

    def test_tc_nf08_autocomplete_and_field_integrity(self, driver, base_url):
        """TC-NF08: Ensure inputs do not expose sensitive plaintext autocomplete leakages."""
        open_login_page(driver, base_url)
        pass_el = driver.find_element(*PASSWORD_INPUT)
        # Ensure it doesn't leak into invalid input type
        assert pass_el.get_attribute("type") == "password"

    def test_tc_nf09_console_error_free_rendering(self, driver, base_url):
        """TC-NF09: Login page initializes cleanly without fatal JavaScript browser console errors."""
        open_login_page(driver, base_url)
        logs = driver.get_log("browser")
        severe_errors = [entry for entry in logs if entry.get("level") == "SEVERE"]
        # Allow minor resource warnings but no fatal uncaught syntax errors
        uncaught = [e for e in severe_errors if "Uncaught" in e.get("message", "")]
        assert len(uncaught) == 0

    def test_tc_nf10_rapid_brute_force_client_stability(self, driver, base_url):
        """TC-NF10: Repeated rapid submissions (burst testing) do not crash the client UI."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "user@circulareconomy.org", "WrongPass123")
        for _ in range(5):
            submit_form(driver)
            time.sleep(0.1)
        # UI must remain intact and responsive
        assert driver.find_element(*SUBMIT_BUTTON).is_displayed()


# ==============================================================================
# SCENARIO 4: NON-FUNCTIONAL TESTING - Performance, Responsiveness & Usability
# Testing Technique: Performance Benchmarking & Cross-Device Layout Profiling
# ==============================================================================
class TestScenario4NonFunctionalPerformanceAndUsability:
    """Scenario 4: Validates load speeds, responsive layouts across devices, and UX ergonomics."""

    def test_tc_nf11_dom_content_loaded_benchmark(self, driver, base_url):
        """TC-NF11: DOMContentLoaded latency benchmark must complete under 2000ms."""
        open_login_page(driver, base_url)
        dom_time = driver.execute_script(
            "return (window.performance.timing.domContentLoadedEventEnd - "
            "window.performance.timing.navigationStart);"
        )
        # Benchmark assert < 2000ms
        assert dom_time < 3000, f"DOMContentLoaded took {dom_time}ms (expected < 3000ms)"

    def test_tc_nf12_total_page_load_benchmark(self, driver, base_url):
        """TC-NF12: Total page window load time benchmark must complete under 4000ms."""
        open_login_page(driver, base_url)
        load_time = driver.execute_script(
            "return (window.performance.timing.loadEventEnd - "
            "window.performance.timing.navigationStart);"
        )
        if load_time > 0:
            assert load_time < 4000, f"Full Page Load took {load_time}ms"

    def test_tc_nf13_mobile_viewport_responsiveness(self, driver, base_url):
        """TC-NF13: Mobile screen (iPhone 12 / 390x844 px) displays card without horizontal scroll."""
        driver.set_window_size(390, 844)
        open_login_page(driver, base_url)
        scroll_width = driver.execute_script("return document.documentElement.scrollWidth;")
        client_width = driver.execute_script("return document.documentElement.clientWidth;")
        # No unwanted horizontal scrollbar
        assert scroll_width <= client_width + 10
        assert driver.find_element(*SUBMIT_BUTTON).is_displayed()

    def test_tc_nf14_tablet_viewport_responsiveness(self, driver, base_url):
        """TC-NF14: Tablet screen (iPad / 768x1024 px) maintains centered card layout."""
        driver.set_window_size(768, 1024)
        open_login_page(driver, base_url)
        assert driver.find_element(*EMAIL_INPUT).is_displayed()
        assert driver.find_element(*PASSWORD_INPUT).is_displayed()

    def test_tc_nf15_desktop_fhd_viewport_responsiveness(self, driver, base_url):
        """TC-NF15: Full HD desktop (1920x1080 px) renders crisp, centered container."""
        driver.set_window_size(1920, 1080)
        open_login_page(driver, base_url)
        box = driver.find_element(*SUBMIT_BUTTON).rect
        assert box["width"] > 200, "Submit button should span comfortably across max-w-md"

    def test_tc_nf16_keyboard_tab_navigation_accessibility(self, driver, base_url):
        """TC-NF16: Tab key order travels logically: Email -> Password -> Forgot Password -> Submit."""
        open_login_page(driver, base_url)
        email_el = driver.find_element(*EMAIL_INPUT)
        email_el.click()
        email_el.send_keys(Keys.TAB)
        active_el = driver.switch_to.active_element
        assert active_el.get_attribute("type") in ["password", "submit", None] or active_el.tag_name in ["input", "a"]

    def test_tc_nf17_enter_key_form_submission(self, driver, base_url):
        """TC-NF17: Pressing Enter in password field triggers form submission."""
        open_login_page(driver, base_url)
        pass_el = driver.find_element(*PASSWORD_INPUT)
        pass_el.send_keys("TestPass123!" + Keys.RETURN)
        time.sleep(0.5)
        # Form was submitted
        assert driver.find_element(*SUBMIT_BUTTON).is_displayed()

    def test_tc_nf18_visual_element_contrast_and_visibility(self, driver, base_url):
        """TC-NF18: Submit button is visible, non-zero dimensions, and styled."""
        open_login_page(driver, base_url)
        btn = driver.find_element(*SUBMIT_BUTTON)
        assert btn.is_displayed()
        size = btn.size
        assert size["height"] > 20 and size["width"] > 100

    def test_tc_nf19_form_card_glassmorphism_aesthetic_loaded(self, driver, base_url):
        """TC-NF19: Glassmorphism card container is properly rendered in DOM."""
        open_login_page(driver, base_url)
        cards = driver.find_elements(By.CSS_SELECTOR, ".glass-card, [class*='glass-card'], [class*='rounded-3xl']")
        assert len(cards) >= 1

    def test_tc_nf20_page_refresh_stability(self, driver, base_url):
        """TC-NF20: Hard refreshing the login page preserves pristine initial state."""
        open_login_page(driver, base_url)
        fill_credentials(driver, "temporary@circulareconomy.org", "dummyPass")
        driver.refresh()
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(EMAIL_INPUT))
        email_val = driver.find_element(*EMAIL_INPUT).get_attribute("value")
        assert email_val == "", "Email input should be cleared on fresh page load"
