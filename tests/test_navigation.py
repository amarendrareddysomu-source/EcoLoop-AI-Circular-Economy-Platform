import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestNavigation:
    """End-to-End Route Navigation and Access Guard Tests."""

    def test_tc_nav01_navigate_to_inventory_page(self, logged_in_driver, base_url):
        """TC-NAV01: Navigating to /inventory renders the Inventory catalog interface."""
        logged_in_driver.get(f"{base_url}/inventory")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //main"))
        )
        assert "/inventory" in logged_in_driver.current_url

    def test_tc_nav02_navigate_to_transactions_page(self, logged_in_driver, base_url):
        """TC-NAV02: Navigating to /transactions renders the Circular Transactions ledger."""
        logged_in_driver.get(f"{base_url}/transactions")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //main"))
        )
        assert "/transactions" in logged_in_driver.current_url

    def test_tc_nav03_navigate_to_ai_predictions_page(self, logged_in_driver, base_url):
        """TC-NAV03: Navigating to /ai-predictions renders the AI Decision Engine."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        WebDriverWait(logged_in_driver, 6).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(., 'AI Circular Decision Engine')]"))
        )
        assert "/ai-predictions" in logged_in_driver.current_url

    def test_tc_nav04_navigate_to_impact_passports(self, logged_in_driver, base_url):
        """TC-NAV04: Navigating to /impact-passports renders the Digital Product Passport page."""
        logged_in_driver.get(f"{base_url}/impact-passports")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //main"))
        )
        assert "/impact-passports" in logged_in_driver.current_url

    def test_tc_nav05_navigate_to_pickup_partners(self, logged_in_driver, base_url):
        """TC-NAV05: Navigating to /pickup-partners renders the Partner Network Finder."""
        logged_in_driver.get(f"{base_url}/pickup-partners")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //main"))
        )
        assert "/pickup-partners" in logged_in_driver.current_url

    def test_tc_nav06_navigate_to_repair_guide(self, logged_in_driver, base_url):
        """TC-NAV06: Navigating to /repair-guide renders the Circular Repair Tutorials."""
        logged_in_driver.get(f"{base_url}/repair-guide")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //main"))
        )
        assert "/repair-guide" in logged_in_driver.current_url

    def test_tc_nav07_navigate_to_rewards_store(self, logged_in_driver, base_url):
        """TC-NAV07: Navigating to /rewards-store renders EcoCredits redemption options."""
        logged_in_driver.get(f"{base_url}/rewards-store")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //main"))
        )
        assert "/rewards-store" in logged_in_driver.current_url

    def test_tc_nav08_navigate_to_reports_page(self, logged_in_driver, base_url):
        """TC-NAV08: Navigating to /reports renders the ESG and analytics reports view."""
        logged_in_driver.get(f"{base_url}/reports")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //main"))
        )
        assert "/reports" in logged_in_driver.current_url

    def test_tc_nav09_admin_portal_navigation(self, admin_driver, base_url):
        """TC-NAV09: Admin user can navigate directly to /admin-dashboard."""
        admin_driver.get(f"{base_url}/admin-dashboard")
        WebDriverWait(admin_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //main"))
        )
        assert "/admin-dashboard" in admin_driver.current_url

    def test_tc_nav10_unauthenticated_guard_on_protected_routes(self, driver, base_url):
        """TC-NAV10: Accessing /inventory without authentication redirects to /login."""
        driver.get(f"{base_url}/inventory")
        WebDriverWait(driver, 6).until(EC.url_contains("/login"))
        assert "/login" in driver.current_url
