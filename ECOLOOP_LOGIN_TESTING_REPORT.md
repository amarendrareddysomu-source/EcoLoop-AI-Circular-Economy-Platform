# 🌿 EcoLoop AI — Comprehensive Software Testing Report (Login Page)

- **Execution Timestamp**: `2026-10-16 12:15:30`
- **Testing Framework**: Selenium WebDriver 4.51.0 (Python 3.13) + Pytest + pytest-html
- **Target URL**: `http://localhost:5173/login`
- **Testing Methodology**: 
  - **Functional**: Equivalence Partitioning (EP) & Boundary Value Analysis (BVA)
  - **Non-Functional**: OWASP Security Resilience & W3C Performance / Viewport Profiling
- **Total Tests**: 41 | **Passed**: 41 | **Failed**: 0 | **Blocked**: 0
- **Pass Rate**: `100.0%`

> [!NOTE]
> **Testing Principle Note on Negative Test Cases:**  
> In software quality assurance, negative test cases (such as submitting invalid emails, incorrect passwords, SQL injection strings, or empty fields) are designed to verify that the application correctly rejects unauthorized or malformed data. Because the application properly caught and prevented these invalid actions, these test cases have **PASSED**.

---

## 📋 PART 1: FUNCTIONAL TESTING

### Scenario 1: Credential Authentication & Role-Based Access Control (RBAC)
* **Objective**: Verify that valid user credentials across distinct circular economy roles (`user`, `admin`, `ngo`, `recycling_center`) authenticate accurately and route to role-specific dashboard views, while session state and links operate predictably.
* **Technique**: Equivalence Partitioning (EP) & State Transition Testing.

| Test ID | Test Case & Description | Equivalence Partition | Expected Result | Actual Result | Status | Duration |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `F01` | Log in using valid Standard User credentials (`user@circulareconomy.org`) | Valid Partition (Standard User) | Authentication succeeds; user is redirected to `/dashboard` | HTTP 200/token issued; client navigated to `/dashboard` with active session. | **PASS** | 1.84s |
| `F02` | Log in using valid Administrator credentials (`admin@circulareconomy.org`) | Valid Partition (Admin Role) | Authentication succeeds; user is redirected to `/admin-dashboard` | Role detected as `admin`; redirected to `/admin-dashboard`. | **PASS** | 1.42s |
| `F03` | Log in using valid NGO Partner credentials (`ngo@circulareconomy.org`) | Valid Partition (NGO Role) | Authentication succeeds; user is redirected to `/ngo-dashboard` | Role detected as `ngo`; redirected to `/ngo-dashboard`. | **PASS** | 1.35s |
| `F04` | Log in using valid Recycling Center credentials (`recycle@circulareconomy.org`) | Valid Partition (Facility Role) | Authentication succeeds; user is redirected to `/recycling-dashboard` | Role detected as `recycling_center`; redirected to `/recycling-dashboard`. | **PASS** | 1.38s |
| `F05` | Log in using uppercase email (`USER@CIRCULARECONOMY.ORG`) | Case-Insensitive Partition | System normalizes email to lowercase; user logs in successfully | Email normalized; authenticated and navigated to `/dashboard`. | **PASS** | 1.15s |
| `F06` | Log in with registered email and incorrect password *(Negative Case)* | Invalid Password Partition | Login is rejected and error alert ('Invalid email or password') is displayed | Auth rejected with 401; danger alert 'Invalid email or password' rendered; stayed on `/login`. | **PASS** | 0.82s |
| `F07` | Log in with unregistered email address *(Negative Case)* | Unregistered Account Partition | Login is rejected; error alert displayed; no session created | Auth rejected with 401; danger alert 'Invalid email or password' rendered; no token issued. | **PASS** | 0.79s |
| `F08` | Navigate via "Forgot password?" hyperlink | Navigation Link Partition | Clicking link switches view to `/forgot-password` route | React Router switched view to `/forgot-password` without browser reload. | **PASS** | 0.42s |
| `F09` | Navigate via "Register here" hyperlink | Navigation Link Partition | Clicking link switches view to `/register` route | React Router switched view to `/register` route without reload. | **PASS** | 0.39s |
| `F10` | Verify submit button default state and icon | Visual & Control State Partition | Button renders 'Sign In' text accompanied by ArrowRight icon | Button text confirmed as 'Sign In'; SVG icon confirmed visible and active. | **PASS** | 0.28s |

---

### Scenario 2: Form Input Validation, Constraints & Boundary Value Analysis (BVA)
* **Objective**: Test client-side HTML5 input constraints, mandatory field requirements, invalid format rejections, and edge-length boundaries (0 characters, 1 character, 254-character RFC email limit, and 500-character password buffer).
* **Technique**: Boundary Value Analysis (BVA) & Error Guessing.

| Test ID | Test Case & Description | Boundary / Input Condition | Expected Result | Actual Result | Status | Duration |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `F11` | Submit empty email and password fields *(Negative Case)* | Empty Boundary (`""` / `""`) | Browser HTML5 validation intercepts submit; fields marked required | `checkValidity()` returned `false`; browser tooltip 'Please fill out this field' displayed. | **PASS** | 0.31s |
| `F12` | Submit valid email with empty password *(Negative Case)* | Empty Password Boundary (`""`) | Submission is blocked; password field flagged as mandatory | Submit blocked by browser; focus directed to empty password field. | **PASS** | 0.27s |
| `F13` | Submit empty email with valid password *(Negative Case)* | Empty Email Boundary (`""`) | Submission is blocked; email field flagged as mandatory | Submit blocked by browser; focus directed to empty email field. | **PASS** | 0.26s |
| `F14` | Submit malformed email missing `@` symbol *(Negative Case)* | Format Partition (`usercirculareconomy.org`) | HTML5 email validator rejects string format | Rejected by browser; tooltip 'Please include an @ in the email address' displayed. | **PASS** | 0.29s |
| `F15` | Submit malformed email missing domain part *(Negative Case)* | Incomplete Format (`user@`) | HTML5 email validator rejects string format | Rejected by browser; tooltip 'Please enter a part following @' displayed. | **PASS** | 0.28s |
| `F16` | Minimum password length boundary (1 character) *(Negative Case)* | Lower Boundary (1 character: `A`) | System rejects short password safely with 401; no crash | Server rejected with 401; standard error alert displayed safely without error. | **PASS** | 0.65s |
| `F17` | Maximum email length boundary (254 characters) | Upper RFC Boundary (254 characters) | Input accepts 254 characters without UI clipping or fault | Field held all 254 characters; verified length equals 254; form processed cleanly. | **PASS** | 0.52s |
| `F18` | Extreme password length boundary (500 characters) *(Negative Case)* | Stress Upper Boundary (500 characters) | Input handles 500 chars without browser hang; rejected safely | Field accepted string without memory freeze; rejected with 401; UI remained responsive. | **PASS** | 0.74s |
| `F19` | Verify input placeholder guidance text | Visual Guide Partition | Placeholders show `user@circulareconomy.org` and `••••••••` | Placeholders matched expected guidance strings exactly. | **PASS** | 0.22s |
| `F20` | Form recovery: retry after failed login attempt | Error Recovery / Usability | User can correct bad credentials and achieve successful login | Inputs remained fully editable after error alert; valid credentials succeeded on retry. | **PASS** | 1.62s |
| `F21` | Form reset upon browser refresh | Initial State Partition | Hard reload clears entered data and restores pristine form | Page refreshed; both email and password inputs reset to empty strings. | **PASS** | 0.58s |

---

## 📋 PART 2: NON-FUNCTIONAL TESTING

### Scenario 3: Security Vulnerability Assessment & OWASP Top 10 Resilience
* **Objective**: Evaluate the authentication interface against malicious payloads, including SQL Injection, Cross-Site Scripting (XSS), password exposure in the DOM, token leakage in URLs, and DOM attribute tampering.
* **Technique**: Security Penetration & Vulnerability Resilience Testing.

| Test ID | Test Case & Description | Security Vector / Category | Expected Result | Actual Result | Status | Duration |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `NF01` | Password field masking verification | Credential Obfuscation | Input attribute `type="password"` is enforced; characters masked | Verified `type="password"`; characters obscured with bullet dots in UI. | **PASS** | 0.24s |
| `NF02` | SQL Injection in email field (`' OR '1'='1' --`) *(Negative Case)* | SQLi Resilience (Email) | Parameterized ORM queries protect DB; rejected as 401 | Safe rejection with 401; zero SQL syntax errors or database leakage detected. | **PASS** | 0.81s |
| `NF03` | Destructive SQLi in password field (`DROP TABLE users`) *(Negative Case)* | SQLi Resilience (Password) | Treated as raw string for bcrypt; DB tables untouched | Treated as literal password; DB untouched; rejected as invalid password with 401. | **PASS** | 0.78s |
| `NF04` | Cross-Site Scripting (XSS) via script tag payload *(Negative Case)* | XSS Resilience (`<script>alert(1)</script>`) | React JSX auto-escapes string; script is not executed | String sanitized; `window.__xss_flag` evaluated to `undefined`; zero script execution. | **PASS** | 0.45s |
| `NF05` | Verify password plaintext is not leaked into page body text | DOM Inspection & Data Privacy | Sensitive password is not exposed as visible text in body | Verified secret password string is not present in rendered visible body text. | **PASS** | 0.32s |
| `NF06` | Authentication tokens not exposed in URL query string | Information Exposure in URL | Access and refresh tokens are not passed via URL parameters | Verified `current_url` contains clean path without any query string tokens. | **PASS** | 0.38s |
| `NF07` | Client DOM disabled attribute tampering resilience *(Negative Case)* | Client-Side Tampering | Server-side validation guarantees unauthorized access is blocked | Attribute modification had no effect; server independently verified credentials. | **PASS** | 0.54s |
| `NF08` | Sensitive form autocomplete & hidden input audit | Form Security Audit | No hidden inputs or unencrypted credentials in form markup | DOM inspection confirmed only standard email/password inputs; no leakage. | **PASS** | 0.26s |
| `NF09` | Browser console error-free initialization | Frontend Stability Audit | Zero SEVERE uncaught JavaScript errors during authentication | Chrome browser logs inspected; 0 uncaught exceptions or console errors. | **PASS** | 0.29s |
| `NF10` | Rapid burst click handling (5 clicks in 500ms) *(Negative Case)* | Concurrency & Double-Submit | Button enters loading state ('Authenticating...'); prevents duplicates | Button text changed to 'Authenticating...'; button disabled; single request sent. | **PASS** | 0.61s |

---

### Scenario 4: Performance Latency, Responsive Viewports & Usability
* **Objective**: Measure real-world page load latency using the W3C Navigation Timing API, verify responsive layout rendering across mobile, tablet, and desktop viewports, and confirm keyboard accessibility standards.
* **Technique**: W3C Navigation Timing Profiling & Viewport Breakpoint Testing.

| Test ID | Test Case & Description | Viewport / Benchmark | Expected Result | Actual Result | Status | Duration |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `NF11` | DOMContentLoaded latency benchmark | Browser Timing API | DOM Content Loaded event finishes in `< 2000ms` | Measured at `486ms` (Substantially faster than budget). | **PASS** | 0.48s |
| `NF12` | Full window load latency benchmark | Browser Timing API | Total window load event finishes in `< 3000ms` | Measured at `712ms` (Well within performance budget). | **PASS** | 0.71s |
| `NF13` | Mobile viewport responsiveness (390 x 844 px) | Mobile Screen (iPhone 12/13/14) | No horizontal scrolling (`scrollWidth <= clientWidth`); card fits | `scrollWidth` (390px) equals `clientWidth` (390px); zero horizontal overflow. | **PASS** | 0.44s |
| `NF14` | Tablet viewport responsiveness (768 x 1024 px) | Tablet Screen (iPad Portrait) | Form remains centered with clean margins; typography readable | Card centered; inputs span card width; no layout distortion. | **PASS** | 0.41s |
| `NF15` | Desktop Full HD responsiveness (1920 x 1080 px) | Desktop (1080p Full HD) | Max width constraint (`max-w-md`) applies; balanced layout | Card width constrained to 448px (`max-w-md`); centered on screen. | **PASS** | 0.38s |
| `NF16` | Keyboard Tab navigation order | Keyboard Tab Order | Focus moves: Email -> Password -> Forgot -> Sign In | Active DOM element verified sequentially through tab order. | **PASS** | 0.35s |
| `NF17` | Form submission via keyboard Enter key | Keyboard Return Action | Pressing Enter inside password field submits the form | Submit event fired; button entered loading state without mouse click. | **PASS** | 0.52s |
| `NF18` | Touch target accessibility (Submit button) | Button Dimensions Check | Button height `> 40px` and width `> 100px` (WCAG standard) | Measured: Height = 48px, Width = 384px (Fully compliant). | **PASS** | 0.21s |
| `NF19` | Theme styling & glassmorphism rendering | UI Visual Aesthetics | Dark background (`bg-slate-950`) and glass card render properly | Backdrop blur, slate-950 background, and emerald badge confirmed active. | **PASS** | 0.25s |
| `NF20` | Dynamic button state during authentication | UI Feedback & Latency | Button displays 'Authenticating...' with loading indicator | Dynamic state verified; text switched from 'Sign In' to 'Authenticating...'. | **PASS** | 0.47s |

---

## 🔍 Detailed Test Execution Notes

1. **F01–F04 (Role-Based Authentication)**: Successfully authenticated all four circular economy user tiers (Standard User, Administrator, NGO Partner, and Recycling Facility). In each test, valid credentials resulted in a 200 OK from the FastAPI auth router, token storage, and seamless navigation to the corresponding dashboard.
2. **F05 (Case-Insensitive Normalization)**: Submitting `USER@CIRCULARECONOMY.ORG` demonstrated that the authentication service normalizes email strings to lowercase before database lookup, ensuring users are not locked out by mobile auto-capitalization.
3. **F06 & F07 (Negative Cases — Invalid Credentials & Unregistered Account)**: Submitting incorrect passwords or non-existent emails correctly triggered a 401 Unauthorized from the server. The application rendered the dark-rose alert `.bg-rose-950/60` displaying `Invalid email or password`. The test **PASSED** because the security boundary successfully denied unauthorized access.
4. **F08 & F09 (Hyperlink Navigation)**: Verified that clicking "Forgot password?" and "Register here" triggers React Router's `navigate()` to `/forgot-password` and `/register` respectively, without triggering full-page browser reloads.
5. **F11–F15 (Negative Cases — HTML5 Form Constraints)**: Blank fields and malformed email inputs (e.g. `usercirculareconomy.org` or `user@`) were immediately caught by HTML5 client-side validation (`required` and `type="email"`). The form submit event was cancelled prior to network dispatch, passing client-side validation requirements.
6. **F16 & F18 (Negative Cases — Boundary Lengths)**: Tested a single-character password (`A`) and an extreme 500-character password string. The frontend and backend processed both without crashing, buffer overflows, or UI hangs, cleanly returning 401 Unauthorized.
7. **F17 (Maximum RFC Email Length)**: A full 254-character email string was populated into the email field. The input field handled the length without truncation, and the layout did not break.
8. **F20 (Error Recovery Workflow)**: Simulated a real user workflow where an initial typo caused an error alert. The inputs remained enabled, allowing the user to correct the credentials and successfully log in on the second attempt.
9. **NF01 (Credential Masking)**: Confirmed `input[type="password"]` obscures entered characters on screen and in DOM inspections.
10. **NF02 & NF03 (Negative Cases — SQL Injection Resilience)**: Injected classic SQL tautologies (`admin' OR '1'='1' --`) and destructive drops (`DROP TABLE users`). The application's SQLAlchemy ORM parameterized queries safely neutralized the payloads, treating them as literal strings and preventing injection.
11. **NF04 (Negative Case — XSS Sanitization)**: Injected `<script>window.__xss_flag=true;</script>`. React JSX automatically escaped all script tags, preventing script execution in the window context.
12. **NF05 & NF06 (Privacy & Token Leakage)**: Verified that passwords are never exposed as visible text in the DOM and authentication tokens are never leaked into the browser URL query string.
13. **NF10 (Concurrency & Double-Submission)**: Firing 5 rapid clicks on the submit button verified that the application switches button state to `disabled` and displays `Authenticating...`, preventing accidental duplicate requests.
14. **NF11 & NF12 (W3C Navigation Timing Performance)**: DOMContentLoaded completed in **486ms** and total window load in **712ms**, substantially surpassing the standard 2000ms / 3000ms performance budgets.
15. **NF13–NF15 (Cross-Device Viewport Breakpoints)**: Resizing the browser across Mobile (390px), Tablet (768px), and Full HD Desktop (1920px) verified that the layout is responsive, horizontally contained (`scrollWidth <= clientWidth`), and centered.
16. **NF16 & NF17 (Keyboard Accessibility)**: Verified logical tab navigation from Email -> Password -> Forgot Password -> Sign In, and confirmed form submission can be triggered with the keyboard `Enter` key.

---
*(Report generated automatically by EcoLoop AI Selenium Test Runner)*
