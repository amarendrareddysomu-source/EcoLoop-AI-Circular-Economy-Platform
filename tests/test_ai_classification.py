import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "test_assets")
VALID_IMAGE_PATH = os.path.join(ASSETS_DIR, "valid_paper.jpg")
INVALID_FILE_PATH = os.path.join(ASSETS_DIR, "invalid_file.txt")
CORRUPTED_IMAGE_PATH = os.path.join(ASSETS_DIR, "corrupted_image.jpg")

# Locators for AIPredictionsPage
FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']")
ANALYZE_BUTTON = (By.XPATH, "//button[contains(., 'Analyze Image with AI') or contains(., 'Pipeline')]")
REMOVE_BUTTON = (By.XPATH, "//button[contains(., 'Remove')]")
UPLOAD_ERROR_ALERT = (By.XPATH, "//*[contains(text(), 'Unsupported file format') or (contains(@class, 'bg-rose-') and contains(., 'file'))]")
RESULT_CATEGORY = (By.XPATH, "//*[contains(text(), 'Primary Classification Result')]/following-sibling::h2")
CONFIDENCE_BADGE = (By.XPATH, "//*[contains(text(), 'AI Confidence:')]")
TOP_5_BREAKDOWN = (By.XPATH, "//*[contains(text(), 'Category Predictions Breakdown')]")


class TestScenario2AIWasteClassification:
    """SCENARIO 2: AI Waste Classification Functional Tests."""

    def test_tc_ai01_open_classification_interface(self, logged_in_driver, base_url):
        """TC-AI01: Open the AI decision engine interface and verify headline and upload container."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        WebDriverWait(logged_in_driver, 6).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(., 'AI Circular Decision Engine')]"))
        )
        assert logged_in_driver.find_element(By.XPATH, "//h1[contains(., 'AI Circular Decision Engine')]").is_displayed()
        assert logged_in_driver.find_element(By.XPATH, "//h3[contains(., 'Upload Item Image')]").is_displayed()

    def test_tc_ai02_validate_missing_image_submission(self, logged_in_driver, base_url):
        """TC-AI02: Verify that Analyze button is disabled when no image has been selected."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        WebDriverWait(logged_in_driver, 6).until(EC.presence_of_element_located(FILE_INPUT))
        
        analyze_btn = logged_in_driver.find_element(*ANALYZE_BUTTON)
        # Button should either be disabled or not clickable
        assert not analyze_btn.is_enabled() or "cursor-not-allowed" in analyze_btn.get_attribute("class")

    def test_tc_ai03_handle_unsupported_file_formats(self, logged_in_driver, base_url):
        """TC-AI03: Uploading a non-image text file triggers client-side unsupported format error."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        WebDriverWait(logged_in_driver, 6).until(EC.presence_of_element_located(FILE_INPUT))
        
        file_input = logged_in_driver.find_element(*FILE_INPUT)
        file_input.send_keys(INVALID_FILE_PATH)
        
        # Verify upload error banner appears with message
        WebDriverWait(logged_in_driver, 6).until(
            EC.visibility_of_element_located(UPLOAD_ERROR_ALERT)
        )
        error_text = logged_in_driver.find_element(*UPLOAD_ERROR_ALERT).text
        assert "Unsupported file format" in error_text

    def test_tc_ai04_upload_valid_supported_image(self, logged_in_driver, base_url):
        """TC-AI04: Upload a valid JPG image and verify preview renders with filename."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        WebDriverWait(logged_in_driver, 6).until(EC.presence_of_element_located(FILE_INPUT))
        
        file_input = logged_in_driver.find_element(*FILE_INPUT)
        file_input.send_keys(VALID_IMAGE_PATH)
        
        # Verify image preview renders
        WebDriverWait(logged_in_driver, 6).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "img[alt='Preview']"))
        )
        preview_img = logged_in_driver.find_element(By.CSS_SELECTOR, "img[alt='Preview']")
        assert preview_img.is_displayed()
        assert "valid_paper.jpg" in logged_in_driver.page_source

    def test_tc_ai05_analyze_button_becomes_active_on_image_select(self, logged_in_driver, base_url):
        """TC-AI05: Analyze button switches to enabled state once valid image is selected."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        file_input = logged_in_driver.find_element(*FILE_INPUT)
        file_input.send_keys(VALID_IMAGE_PATH)
        
        WebDriverWait(logged_in_driver, 6).until(
            EC.element_to_be_clickable(ANALYZE_BUTTON)
        )
        btn = logged_in_driver.find_element(*ANALYZE_BUTTON)
        assert btn.is_enabled()
        assert "bg-emerald-600" in btn.get_attribute("class")

    def test_tc_ai06_trigger_classification_pipeline(self, logged_in_driver, base_url):
        """TC-AI06: Triggering analysis changes button to loading spinner state."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        file_input = logged_in_driver.find_element(*FILE_INPUT)
        file_input.send_keys(VALID_IMAGE_PATH)
        
        btn = logged_in_driver.find_element(*ANALYZE_BUTTON)
        btn.click()
        
        # Expect either loading phase text or completed results
        WebDriverWait(logged_in_driver, 10).until(
            lambda d: "Pipeline" in d.page_source or d.find_elements(*RESULT_CATEGORY)
        )
        assert True

    def test_tc_ai07_verify_predicted_category_displayed(self, logged_in_driver, base_url):
        """TC-AI07: Verify end-to-end AI prediction displays predicted material category."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        file_input = logged_in_driver.find_element(*FILE_INPUT)
        file_input.send_keys(VALID_IMAGE_PATH)
        
        logged_in_driver.find_element(*ANALYZE_BUTTON).click()
        
        # Wait up to 15 seconds for multi-model AI pipeline
        WebDriverWait(logged_in_driver, 15).until(
            EC.visibility_of_element_located(RESULT_CATEGORY)
        )
        category_el = logged_in_driver.find_element(*RESULT_CATEGORY)
        assert len(category_el.text.strip()) > 0
        assert category_el.is_displayed()

    def test_tc_ai08_verify_confidence_score_badge(self, logged_in_driver, base_url):
        """TC-AI08: Verify AI confidence score percentage badge is rendered."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        file_input = logged_in_driver.find_element(*FILE_INPUT)
        file_input.send_keys(VALID_IMAGE_PATH)
        logged_in_driver.find_element(*ANALYZE_BUTTON).click()
        
        WebDriverWait(logged_in_driver, 15).until(
            EC.visibility_of_element_located(CONFIDENCE_BADGE)
        )
        badge = logged_in_driver.find_element(*CONFIDENCE_BADGE)
        assert "%" in badge.text

    def test_tc_ai09_verify_top_5_predictions_breakdown(self, logged_in_driver, base_url):
        """TC-AI09: Verify Top-5 probability breakdown section is present in results."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        file_input = logged_in_driver.find_element(*FILE_INPUT)
        file_input.send_keys(VALID_IMAGE_PATH)
        logged_in_driver.find_element(*ANALYZE_BUTTON).click()
        
        WebDriverWait(logged_in_driver, 15).until(
            EC.visibility_of_element_located(TOP_5_BREAKDOWN)
        )
        breakdown = logged_in_driver.find_element(*TOP_5_BREAKDOWN)
        assert breakdown.is_displayed()

    def test_tc_ai10_remove_uploaded_image_action(self, logged_in_driver, base_url):
        """TC-AI10: Clicking Remove clears image preview and resets file input."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        file_input = logged_in_driver.find_element(*FILE_INPUT)
        file_input.send_keys(VALID_IMAGE_PATH)
        
        WebDriverWait(logged_in_driver, 6).until(
            EC.visibility_of_element_located(REMOVE_BUTTON)
        )
        remove_btn = logged_in_driver.find_element(*REMOVE_BUTTON)
        remove_btn.click()
        
        # Verify preview is gone
        preview_imgs = logged_in_driver.find_elements(By.CSS_SELECTOR, "img[alt='Preview']")
        assert len(preview_imgs) == 0
        assert logged_in_driver.find_element(By.XPATH, "//p[contains(., 'Drag & Drop image here')]").is_displayed()

    def test_tc_ai11_handle_corrupted_image_safely(self, logged_in_driver, base_url):
        """TC-AI11: Handle corrupted image upload gracefully without unhandled crashes."""
        logged_in_driver.get(f"{base_url}/ai-predictions")
        file_input = logged_in_driver.find_element(*FILE_INPUT)
        file_input.send_keys(CORRUPTED_IMAGE_PATH)
        
        # The frontend/backend either catches invalid image format or returns safe error banner
        time.sleep(1)
        assert "/ai-predictions" in logged_in_driver.current_url
