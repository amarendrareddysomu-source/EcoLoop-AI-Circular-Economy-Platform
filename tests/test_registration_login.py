import time
import uuid
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Locators for Registration Page
REG_FULLNAME_INPUT = (By.CSS_SELECTOR, "input[name='full_name']")
REG_EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
REG_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
REG_ROLE_SELECT = (By.CSS_SELECTOR, "select[name='role']")
REG_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
REG_ERROR_ALERT = (By.CSS_SELECTOR, ".bg-rose-950\\/60, [class*='text-rose-300']")
REG_SIGNIN_LINK = (By.XPATH, "//a[contains(text(), 'Sign In')]")

# Locators for Login Page
LOGIN_EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
LOGIN_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
LOGIN_ERROR_ALERT = (By.CSS_SELECTOR, ".bg-rose-950\\/60, [class*='text-rose-300']")


class TestScenario1RegistrationLogin:
    """SCENARIO 1: Registration, Login, and Access Control Functional Tests."""

    def test_tc_rl01_open_registration_page(self, driver, base_url):
        """TC-RL01: Open registration page and verify essential form elements."""
        driver.get(f"{base_url}/register")
        WebDriverWait(driver, 6).until(
            EC.visibility_of_element_located(REG_FULLNAME_INPUT)
        )
        assert driver.find_element(*REG_EMAIL_INPUT).is_displayed()
        assert driver.find_element(*REG_PASSWORD_INPUT).is_displayed()
        assert driver.find_element(*REG_ROLE_SELECT).is_displayed()
        assert driver.find_element(*REG_SUBMIT_BUTTON).is_displayed()
        assert "Create Account" in driver.page_source

    def test_tc_rl02_register_with_valid_information(self, driver, base_url):
        """TC-RL02: Register a new account with valid unique credentials."""
        unique_id = uuid.uuid4().hex[:8]
        test_email = f"qa_user_{unique_id}@circulareconomy.org"
        
        driver.get(f"{base_url}/register")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(REG_FULLNAME_INPUT))
        
        driver.find_element(*REG_FULLNAME_INPUT).send_keys(f"QA Tester {unique_id}")
        driver.find_element(*REG_EMAIL_INPUT).send_keys(test_email)
        driver.find_element(*REG_PASSWORD_INPUT).send_keys("SecurePassword123!")
        
        # Select User role
        role_select = Select(driver.find_element(*REG_ROLE_SELECT))
        role_select.select_by_value("user")
        
        driver.find_element(*REG_SUBMIT_BUTTON).click()
        
        # Expect redirect to login page with registered=true parameter
        WebDriverWait(driver, 6).until(EC.url_contains("/login"))
        assert "/login" in driver.current_url

    def test_tc_rl03_reject_malformed_email_on_register(self, driver, base_url):
        """TC-RL03: Reject invalid or malformed email address on registration form."""
        driver.get(f"{base_url}/register")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(REG_FULLNAME_INPUT))
        
        driver.find_element(*REG_FULLNAME_INPUT).send_keys("Test Malformed")
        email_el = driver.find_element(*REG_EMAIL_INPUT)
        email_el.send_keys("invalidemailformat")
        driver.find_element(*REG_PASSWORD_INPUT).send_keys("ValidPass123!")
        driver.find_element(*REG_SUBMIT_BUTTON).click()
        
        # Browser HTML5 email validation prevents dispatch
        is_valid = driver.execute_script("return arguments[0].checkValidity();", email_el)
        assert is_valid is False
        assert "/register" in driver.current_url

    def test_tc_rl04_validate_required_registration_fields(self, driver, base_url):
        """TC-RL04: Submitting an empty registration form is blocked by required validators."""
        driver.get(f"{base_url}/register")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(REG_FULLNAME_INPUT))
        
        name_el = driver.find_element(*REG_FULLNAME_INPUT)
        driver.find_element(*REG_SUBMIT_BUTTON).click()
        
        is_valid = driver.execute_script("return arguments[0].checkValidity();", name_el)
        assert is_valid is False
        assert "/register" in driver.current_url

    def test_tc_rl05_password_length_constraint_validation(self, driver, base_url):
        """TC-RL05: Password under minimum 8-character constraint is rejected by HTML5 validation."""
        driver.get(f"{base_url}/register")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(REG_FULLNAME_INPUT))
        
        driver.find_element(*REG_FULLNAME_INPUT).send_keys("Short Pass User")
        driver.find_element(*REG_EMAIL_INPUT).send_keys("shortpass@circulareconomy.org")
        pass_el = driver.find_element(*REG_PASSWORD_INPUT)
        pass_el.send_keys("12345")  # Less than minlength 8
        driver.find_element(*REG_SUBMIT_BUTTON).click()
        
        is_valid = driver.execute_script("return arguments[0].checkValidity();", pass_el)
        assert is_valid is False
        assert "/register" in driver.current_url

    def test_tc_rl06_handle_duplicate_registration(self, driver, base_url):
        """TC-RL06: Attempting to register an already existing email returns an error alert."""
        driver.get(f"{base_url}/register")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(REG_FULLNAME_INPUT))
        
        # Use existing account from seed
        driver.find_element(*REG_FULLNAME_INPUT).send_keys("Existing User")
        driver.find_element(*REG_EMAIL_INPUT).send_keys("user@circulareconomy.org")
        driver.find_element(*REG_PASSWORD_INPUT).send_keys("Password123!")
        driver.find_element(*REG_SUBMIT_BUTTON).click()
        
        # Expect error banner on page
        WebDriverWait(driver, 6).until(
            EC.visibility_of_element_located(REG_ERROR_ALERT)
        )
        alert = driver.find_element(*REG_ERROR_ALERT)
        assert "already registered" in alert.text.lower() or "failed" in alert.text.lower()
        assert "/register" in driver.current_url

    def test_tc_rl07_login_using_valid_credentials(self, driver, base_url):
        """TC-RL07: Log in with valid standard user credentials and verify redirect to /dashboard."""
        driver.get(f"{base_url}/login")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(LOGIN_EMAIL_INPUT))
        
        driver.find_element(*LOGIN_EMAIL_INPUT).send_keys("user@circulareconomy.org")
        driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys("Password123!")
        driver.find_element(*LOGIN_SUBMIT_BUTTON).click()
        
        WebDriverWait(driver, 6).until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url

    def test_tc_rl08_reject_invalid_credentials(self, driver, base_url):
        """TC-RL08: Log in with incorrect password produces danger alert and denies access."""
        driver.get(f"{base_url}/login")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(LOGIN_EMAIL_INPUT))
        
        driver.find_element(*LOGIN_EMAIL_INPUT).send_keys("user@circulareconomy.org")
        driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys("TotallyWrongPassword999!")
        driver.find_element(*LOGIN_SUBMIT_BUTTON).click()
        
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(LOGIN_ERROR_ALERT))
        alert_el = driver.find_element(*LOGIN_ERROR_ALERT)
        assert "email or password" in alert_el.text.lower()
        assert "/login" in driver.current_url

    def test_tc_rl09_validate_empty_login_fields(self, driver, base_url):
        """TC-RL09: Submitting blank login form is intercepted by client-side required validation."""
        driver.get(f"{base_url}/login")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(LOGIN_EMAIL_INPUT))
        
        email_el = driver.find_element(*LOGIN_EMAIL_INPUT)
        driver.find_element(*LOGIN_SUBMIT_BUTTON).click()
        
        is_valid = driver.execute_script("return arguments[0].checkValidity();", email_el)
        assert is_valid is False
        assert "/login" in driver.current_url

    def test_tc_rl10_login_navigation_and_access_to_admin_portal(self, driver, base_url):
        """TC-RL10: Valid administrator credentials route strictly to /admin-dashboard."""
        driver.get(f"{base_url}/login")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(LOGIN_EMAIL_INPUT))
        
        driver.find_element(*LOGIN_EMAIL_INPUT).send_keys("admin_test@circulareconomy.org")
        driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys("AdminPass123!")
        driver.find_element(*LOGIN_SUBMIT_BUTTON).click()
        
        WebDriverWait(driver, 6).until(EC.url_contains("/admin-dashboard"))
        assert "/admin-dashboard" in driver.current_url

    def test_tc_rl11_protected_route_access_control(self, driver, base_url):
        """TC-RL11: Directly accessing /dashboard without a session redirects back to /login."""
        driver.get(f"{base_url}/dashboard")
        # ProtectedRoute redirects unauthenticated users to /login
        WebDriverWait(driver, 6).until(EC.url_contains("/login"))
        assert "/login" in driver.current_url
