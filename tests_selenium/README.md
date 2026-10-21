# Automated Selenium Testing Suite for Login Page

This directory contains a complete, automated test suite built with **Selenium WebDriver (Python)**, **pytest**, and **pytest-html** for the **EcoLoop Circular Economy Platform Login Page**.

---

## 1. Selected Software Testing Techniques

### Functional Testing Technique:
- **Equivalence Partitioning (EP)**:
  - Divides input domains into valid classes (e.g., valid email formats, registered accounts, role-specific accounts) and invalid classes (e.g., malformed emails, wrong passwords, unverified users).
- **Boundary Value Analysis (BVA)**:
  - Tests the extreme boundary conditions: minimum length (1 character), extreme maximum lengths (254-character emails, 500-character passwords), and empty (null) strings.

### Non-Functional Testing Technique:
- **Security Vulnerability Assessment (OWASP Top 10 vectors)**:
  - Tests SQL injection resilience, Cross-Site Scripting (XSS) payload sanitization, password masking, token protection in URLs, and DOM inspection leaks.
- **Performance & Usability Benchmarking**:
  - Tests DOMContentLoaded and Window Load latency using the browser's native Navigation Timing API, cross-device responsive layout checks (mobile, tablet, desktop), and keyboard accessibility.

---

## 2. Test Suite Architecture

| Scenario | Category | Description | Count |
|---|---|---|---|
| **Scenario 1** | Functional | Credential Authentication, Role Routing & Navigation | 10 Test Cases |
| **Scenario 2** | Functional | Input Validation, Error Handling & Boundary Value Analysis | 10 Test Cases |
| **Scenario 3** | Non-Functional | Security, OWASP Injection Resilience & DOM Integrity | 10 Test Cases |
| **Scenario 4** | Non-Functional | Performance Latency, Responsive Viewports & Usability | 10 Test Cases |
| **Total** | | | **40 Test Cases** |

---

## 3. How to Run the Tests & See Results

### Prerequisites
Make sure your frontend (and backend, if testing live authentication) is running:
```bash
# Terminal 1: Start frontend
cd frontend
npm run dev
# (Runs by default at http://localhost:5173)

# Terminal 2: Start backend (optional for live user login)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Running the Selenium Test Suite
Run the tests using the Python virtual environment in `backend/venv`:

```bash
# Headless mode (fast, runs in background) with interactive HTML report
./backend/venv/bin/pytest tests_selenium/test_login_suite.py \
  --base-url=http://localhost:5173 \
  --html=tests_selenium/report.html \
  --self-contained-html -v

# Or visible (headed) browser mode to watch Chrome perform the actions
./backend/venv/bin/pytest tests_selenium/test_login_suite.py \
  --base-url=http://localhost:5173 \
  --headed -v
```

### How to View the Results
1. **Terminal Console Output**:
   - Pytest prints real-time status with green `.` for passes, red `F` for failures, and elapsed execution times.
2. **Interactive HTML Test Report**:
   - Open `tests_selenium/report.html` in your web browser:
     ```bash
     open tests_selenium/report.html
     ```
   - Includes:
     - Pass/Fail summary bar chart
     - Expandable test case execution logs
     - Environment metadata (Python version, OS, browser version)
3. **Automated Failure Screenshots**:
   - If any test fails, an automatic screenshot is captured and saved inside `tests_selenium/screenshots/` and embedded directly into the HTML report.
