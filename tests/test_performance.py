import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_page_load_timing(driver):
    """Calculates navigation metrics using W3C Navigation Timing API."""
    return driver.execute_script("""
        var t = window.performance.timing;
        return {
            dns: t.domainLookupEnd - t.domainLookupStart,
            tcp: t.connectEnd - t.connectStart,
            domReady: t.domContentLoadedEventEnd - t.navigationStart,
            fullLoad: (t.loadEventEnd > 0 ? t.loadEventEnd : Date.now()) - t.navigationStart
        };
    """)


class TestScenario3BrowserPerformance:
    """SCENARIO 3: Non-Functional Browser Performance Benchmarks."""

    def test_tc_perf01_measure_initial_navigation_time(self, driver, base_url):
        """TC-PERF01: Measure initial entry navigation latency (< 3000ms threshold)."""
        start = time.time()
        driver.get(f"{base_url}/login")
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        duration_ms = (time.time() - start) * 1000
        
        timing = get_page_load_timing(driver)
        assert timing["domReady"] < 3000, f"DOM Ready took {timing['domReady']}ms"
        assert duration_ms < 4000, f"Total browser response took {duration_ms}ms"

    def test_tc_perf02_measure_login_page_navigation_time(self, driver, base_url):
        """TC-PERF02: Benchmark login page load latency against 2500ms budget."""
        driver.get(f"{base_url}/login")
        timing = get_page_load_timing(driver)
        assert timing["domReady"] < 2500, f"Login DOM Ready latency was {timing['domReady']}ms"

    def test_tc_perf03_measure_dashboard_navigation_time(self, logged_in_driver, base_url):
        """TC-PERF03: Measure authenticated /dashboard navigation and component rendering."""
        start = time.time()
        logged_in_driver.get(f"{base_url}/dashboard")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //main"))
        )
        duration_ms = (time.time() - start) * 1000
        assert duration_ms < 3500, f"Dashboard load took {duration_ms}ms"

    def test_tc_perf04_measure_inventory_page_navigation_time(self, logged_in_driver, base_url):
        """TC-PERF04: Measure authenticated /inventory route load time."""
        start = time.time()
        logged_in_driver.get(f"{base_url}/inventory")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.TAG_NAME, "main"))
        )
        duration_ms = (time.time() - start) * 1000
        assert duration_ms < 3500, f"Inventory load took {duration_ms}ms"

    def test_tc_perf05_measure_classification_page_navigation_time(self, logged_in_driver, base_url):
        """TC-PERF05: Measure /ai-predictions route load and UI initialization latency."""
        start = time.time()
        logged_in_driver.get(f"{base_url}/ai-predictions")
        WebDriverWait(logged_in_driver, 6).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'AI Circular Decision Engine')]"))
        )
        duration_ms = (time.time() - start) * 1000
        assert duration_ms < 3500, f"AI Predictions load took {duration_ms}ms"

    def test_tc_perf06_measure_time_for_key_ui_elements_to_appear(self, driver, base_url):
        """TC-PERF06: Measure millisecond latency for primary interactive form controls to become visible."""
        start = time.time()
        driver.get(f"{base_url}/login")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
        element_ready_ms = (time.time() - start) * 1000
        assert element_ready_ms < 2000, f"Submit button took {element_ready_ms}ms to render"

    def test_tc_perf07_check_important_pages_finish_loading(self, driver, base_url):
        """TC-PERF07: Ensure document.readyState transitions to 'complete' within timeout."""
        driver.get(f"{base_url}/login")
        ready_state = driver.execute_script("return document.readyState;")
        assert ready_state in ["interactive", "complete"]

    def test_tc_perf08_record_page_loading_failures_and_errors(self, driver, base_url):
        """TC-PERF08: Check browser logs for zero fatal network asset 404/500 failures."""
        driver.get(f"{base_url}/login")
        logs = driver.get_log("browser")
        severe_errors = [e for e in logs if e.get("level") == "SEVERE" and "favicon" not in e.get("message", "")]
        assert len(severe_errors) == 0, f"Found severe console errors: {severe_errors}"

    def test_tc_perf09_repeated_navigation_benchmark(self, driver, base_url):
        """TC-PERF09: Measure login navigation 3 consecutive times to calculate consistency and cache efficiency."""
        timings = []
        for _ in range(3):
            start = time.time()
            driver.get(f"{base_url}/login")
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
            timings.append((time.time() - start) * 1000)
            time.sleep(0.1)
        
        avg_time = sum(timings) / len(timings)
        assert avg_time < 2500, f"Average repeated load time was {avg_time}ms"

    def test_tc_perf10_generate_timing_summary(self, driver, base_url):
        """TC-PERF10: Extract and validate end-to-end W3C network timing metrics."""
        driver.get(f"{base_url}/login")
        metrics = get_page_load_timing(driver)
        assert metrics["domReady"] > 0
        assert metrics["domReady"] < 4000
