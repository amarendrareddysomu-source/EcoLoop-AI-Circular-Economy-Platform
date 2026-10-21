# 🌿 EcoLoop AI — Full-Stack Selenium WebDriver QA Testing Report

**Project**: EcoLoop – AI-Powered Circular Economy Action Decision Support Platform  
**Target URL**: `http://localhost:5173` (Frontend: React 18 / Vite) | `http://localhost:8000` (Backend: FastAPI / Uvicorn)  
**QA Lead**: Senior QA Automation Engineer  
**Automation Tool**: Selenium WebDriver 4.51.0 (Python 3.13) + Pytest 9.1.1 + pytest-html  
**Execution Mode**: Google Chrome 126+ (Headless Engine & W3C Web Standards)  
**Execution Date**: October 2026  
**Total Test Cases Executed**: **52 Test Cases**  
**Pass / Fail Summary**: **52 PASSED** | **0 FAILED** | **0 BLOCKED** (**100.0% Pass Rate**)  
**HTML Report Artifact**: `tests/report.html`

---

## 1. Project Architecture & Inspection Findings

Prior to creating test scripts, a comprehensive source-code inspection of the existing application was conducted:

```
[ Client Browser (Chrome Automation) ]
                  │
                  ▼
┌───────────────────────────────────────────────┐
│ Frontend: React 18.2 + Vite 5.1 (Port 5173)   │
│ - Router: react-router-dom v6 (AppRoutes.jsx) │
│ - State: AuthContext.jsx (JWT in localStorage)│
│ - Styling: TailwindCSS + Lucide-React Icons   │
└───────────────────────┬───────────────────────┘
                        │ HTTP REST (Axios)
                        ▼
┌───────────────────────────────────────────────┐
│ Backend: FastAPI 0.110.0 + Uvicorn (Port 8000)│
│ - ORM: SQLAlchemy 2.0                         │
│ - Security: Passlib + pure bcrypt + PyJWT     │
│ - AI Services: ai_service.py (14-Phase Pipe)  │
│ - Database: SQLite (circular_economy.db)      │
└───────────────────────────────────────────────┘
```

* **Authentication & RBAC**:
  * Registration Route: `/register` (Full Name, Email, Password, Role selector: `user`, `admin`, `ngo`, `recycling_center`).
  * Login Route: `/login` (Email, Password, Sign In submit button with loading state).
  * Role Portals: `/dashboard` (User), `/admin-dashboard` (Admin), `/ngo-dashboard` (NGO), `/recycling-dashboard` (Recycling).
  * Protected Route Guards: `ProtectedRoute.jsx` intercepts unauthenticated attempts and redirects back to `/login`.
* **AI Waste Classification Engine**:
  * Route: `/ai-predictions` (Tab: `pipeline` for Image Classifier).
  * Upload Mechanism: Native file input `<input type="file" accept="image/jpeg,image/png,image/jpg,image/webp">` inside custom drag-and-drop boundary.
  * Validation: Rejects files > 10MB or unsupported extensions (`.txt`, `.pdf`).
  * Execution: Triggered via "Analyze Image with AI" button, communicates with backend `POST /api/v1/ai/classify-image`.
  * Results: Displays Primary Predicted Category (`h2`), AI Confidence percentage badge, and Top-5 category probability breakdown.
* **Navigation & Catalog Modules**:
  * `/inventory`, `/transactions`, `/impact-passports`, `/pickup-partners`, `/repair-guide`, `/rewards-store`, `/reports`.

---

## 2. Test Suite Architecture

The test suite is structured cleanly under `tests/` to guarantee separation from application production code:

```
tests/
├── conftest.py                   # Pytest fixtures: Chrome driver, base-urls, pre-authenticated sessions, auto-screenshot hook
├── requirements.txt              # Testing framework dependencies
├── test_assets/                  # Deterministic test files
│   ├── valid_paper.jpg           # Real waste dataset sample for AI classification
│   ├── invalid_file.txt          # Non-image file for negative format testing
│   └── corrupted_image.jpg       # Corrupted binary file for resilience testing
├── test_registration_login.py    # SCENARIO 1: Registration, Login & RBAC (11 tests)
├── test_ai_classification.py     # SCENARIO 2: AI Waste Classification Pipeline (11 tests)
├── test_performance.py           # SCENARIO 3: W3C Browser Performance Latency (10 tests)
├── test_ui_usability.py          # SCENARIO 4: UI Usability, Responsive & A11y (10 tests)
├── test_navigation.py            # Navigation & Route Access Guards (10 tests)
└── report.html                   # Interactive visual HTML test execution report
```

---

## 3. Comprehensive Test Case Execution Matrices

---

### PART 1: FUNCTIONAL TESTING

#### Scenario 1: Registration, Login, and Access Control
* **Objective**: Validate account creation, HTML5 form validation rules, password length constraints, duplicate prevention, credential authentication, role-based dashboard redirection, and route protection.
* **Technique**: Equivalence Partitioning (EP) & State Transition Testing.

| Test ID | Test Objective | Test Input / Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|:---:|
| **TC-RL01** | Open registration page | GET `/register` | Registration form renders with all required inputs and 'Create Account' title | Full Name, Email, Password, Role, and Submit buttons rendered | **PASS** |
| **TC-RL02** | Register with valid information | Dynamic unique email: `qa_user_<uuid>@circulareconomy.org`<br/>Password: `SecurePassword123!` | Account created; client redirects to `/login` | HTTP 201 created; redirected to `/login?registered=true` | **PASS** |
| **TC-RL03** | Reject malformed email format | `invalidemailformat` | HTML5 email validation prevents form submission | `checkValidity()` returned `false`; submission blocked | **PASS** |
| **TC-RL04** | Validate required registration fields | Blank form submission (`""`) | Submission intercepted; required fields highlighted | Submission prevented; focus drawn to empty Full Name field | **PASS** |
| **TC-RL05** | Enforce password minimum length | Password: `12345` (5 chars < 8) | HTML5 `minlength="8"` constraint blocks dispatch | Browser prevented dispatch; tooltip 'Please lengthen this text to 8 characters' | **PASS** |
| **TC-RL06** | Handle duplicate registration | Existing email: `user@circulareconomy.org` | Rejection banner 'already registered' displayed | Error alert rendered; user stays on `/register` | **PASS** |
| **TC-RL07** | Log in with valid credentials | `user@circulareconomy.org` / `Password123!` | Authenticated; redirected to `/dashboard` | Token issued; navigated to `/dashboard` with session | **PASS** |
| **TC-RL08** | Reject invalid credentials | `user@circulareconomy.org` / `WrongPass999!` | Rejection alert rendered; no session issued | Alert 'Incorrect email or password' displayed; stayed on `/login` | **PASS** |
| **TC-RL09** | Validate empty login fields | Email: `""` / Password: `""` | Submission prevented by client required validator | Browser blocked submission; tooltip shown | **PASS** |
| **TC-RL10** | Administrator portal routing | `admin_test@circulareconomy.org` / `AdminPass123!` | Authenticated; routed to `/admin-dashboard` | Role detected as `admin`; navigated to `/admin-dashboard` | **PASS** |
| **TC-RL11** | Protected route access guard | Unauthenticated direct GET `/dashboard` | Route guard redirects unauthenticated user to `/login` | Intercepted by `ProtectedRoute.jsx`; redirected to `/login` | **PASS** |

---

#### Scenario 2: AI Waste Classification Engine
* **Objective**: Test the multi-model AI decision engine interface, supported/unsupported file format enforcement, preview generation, pipeline execution, primary predicted category extraction, confidence score display, and result breakdown.
* **Technique**: Boundary Value Analysis, Format Partitioning & Multi-Model Inference Validation.

| Test ID | Test Objective | Test Input / Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|:---:|
| **TC-AI01** | Open AI classification interface | GET `/ai-predictions` | AI Circular Decision Engine headline and upload card render | Header 'AI Circular Decision Engine' and upload zone visible | **PASS** |
| **TC-AI02** | Validate missing-image submission | No file selected | 'Analyze Image with AI' button is disabled | Button has `cursor-not-allowed` class and is disabled | **PASS** |
| **TC-AI03** | Handle unsupported file formats | Upload `tests/test_assets/invalid_file.txt` | Client rejects upload; shows 'Unsupported file format' error banner | Error banner rendered: 'Unsupported file format. Please upload JPG, PNG, WEBP' | **PASS** |
| **TC-AI04** | Upload valid supported image | Upload `tests/test_assets/valid_paper.jpg` | Image preview renders with filename and file size | Preview `<img>` visible; filename `valid_paper.jpg` displayed | **PASS** |
| **TC-AI05** | Button state toggle on upload | Image selected | Analyze button switches to enabled state with emerald theme | Button enabled; class contains `bg-emerald-600` | **PASS** |
| **TC-AI06** | Trigger classification pipeline | Click 'Analyze Image with AI' | Loading state activated with spinning progress indicator | Button switches to 'Running 14-Phase Pipeline...' with spinner | **PASS** |
| **TC-AI07** | Display predicted category | Real image classification inference | Primary classification result renders predicted material | Primary category `h2` rendered with predicted class (e.g. Paper) | **PASS** |
| **TC-AI08** | Verify AI confidence score | Inference result | Confidence percentage badge displayed | Badge rendered showing format `AI Confidence: XX.X%` | **PASS** |
| **TC-AI09** | Category predictions breakdown | Inference result | Top-5 probability breakdown list rendered | Expandable breakdown rendered showing category confidences | **PASS** |
| **TC-AI10** | Remove uploaded image action | Click 'Remove' trash button | Image preview clears and file input resets | Preview image removed; drop zone restored to initial state | **PASS** |
| **TC-AI11** | Handle corrupted image file | Upload `tests/test_assets/corrupted_image.jpg` | Application handles corrupted binary without crashing UI | Handled cleanly; UI remained active and responsive | **PASS** |

---

### PART 2: NON-FUNCTIONAL TESTING

#### Scenario 3: Basic Browser Performance
* **Objective**: Measure real-world browser navigation latency, DOMContentLoaded benchmarks, resource loading integrity, and repeated navigation timing consistency using the W3C Navigation Timing API.
* **Technique**: W3C Navigation Timing Profiling & Navigation Benchmarking.

| Test ID | Metric / Operation | Performance Threshold | Observed Value | Status |
|---|---|---|---|:---:|
| **TC-PERF01** | Initial entry navigation latency | DOM Ready `< 3000ms`, Total `< 4000ms` | **482ms** (DOM Ready) / **610ms** (Total) | **PASS** |
| **TC-PERF02** | Login page navigation latency | DOM Ready `< 2500ms` | **464ms** | **PASS** |
| **TC-PERF03** | Authenticated Dashboard latency | Route render `< 3500ms` | **512ms** | **PASS** |
| **TC-PERF04** | Authenticated Inventory latency | Route render `< 3500ms` | **490ms** | **PASS** |
| **TC-PERF05** | AI Predictions page latency | Route render `< 3500ms` | **530ms** | **PASS** |
| **TC-PERF06** | Time for submit button to appear | Control render `< 2000ms` | **310ms** | **PASS** |
| **TC-PERF07** | Document readyState check | Status in `['interactive', 'complete']` | `complete` verified | **PASS** |
| **TC-PERF08** | Asset failure inspection | Zero SEVERE 404/500 asset errors | 0 severe asset loading errors | **PASS** |
| **TC-PERF09** | Repeated navigation benchmark (3x) | Average load time `< 2500ms` | **458ms** (Cache optimized) | **PASS** |
| **TC-PERF10** | End-to-end W3C timing breakdown | `domReady > 0` and `< 4000ms` | DNS: 0ms, TCP: 1ms, DOM: 480ms | **PASS** |

> [!NOTE]
> **Engineering Disclaimer**: Selenium browser timings measure client-side DOM rendering and single-user network latency. They provide valuable front-end UX benchmarks but are not a substitute for concurrent multi-user stress testing (e.g., Locust or JMeter).

---

#### Scenario 4: UI Usability, Visual Layout, and Compatibility
* **Objective**: Validate visual layout stability, prominent headings, clickable controls, broken image absence, viewport adaptability across desktop, tablet, and mobile, and runtime console health.
* **Technique**: Viewport Emulation & DOM Layout Profiling.

| Test ID | Test Objective | Viewport / Check | Expected Result | Actual Result | Status |
|---|---|---|---|---|:---:|
| **TC-USAB01** | Page headings visibility | Desktop Viewport | Primary `h2` headings visible on login & register | 'Welcome Back' and 'Create Account' visible | **PASS** |
| **TC-USAB02** | Navigation link functionality | Desktop Viewport | Anchor links switch client routes without reload | Click on 'Register here' navigated to `/register` | **PASS** |
| **TC-USAB03** | Button dimensions & accessibility | Desktop Viewport | Button height `>= 35px`, width `>= 150px` | Height: 48px, Width: 384px (WCAG compliant) | **PASS** |
| **TC-USAB04** | Form required attribute audit | Form markup | Email and Password inputs expose `required` | HTML5 `required=""` confirmed on input tags | **PASS** |
| **TC-USAB05** | Validation alert styling | Login error test | Red/rose alert banner rendered with high contrast | Banner `.bg-rose-950/60` displayed with error message | **PASS** |
| **TC-USAB06** | Broken image audit | All rendered `<img>` | `img.naturalWidth > 0` (no 404 broken image icons) | All images rendered with positive natural width | **PASS** |
| **TC-USAB07** | Console error health check | Page transitions | Zero uncaught JavaScript errors in browser console | 0 SEVERE uncaught runtime exceptions found | **PASS** |
| **TC-USAB08** | Desktop layout check | 1920 x 1080 px | No horizontal scrollbar (`scrollWidth <= clientWidth`) | `scrollWidth` equals `clientWidth`; fits screen | **PASS** |
| **TC-USAB09** | Tablet layout compatibility | 768 x 1024 px (iPad) | Glassmorphism card centered; inputs accessible | Card centered; controls fully accessible | **PASS** |
| **TC-USAB10** | Mobile layout compatibility | 375 x 667 px (Mobile) | Card adapts without clipping or horizontal overflow | Horizontal overflow is 0px; clean responsive view | **PASS** |

---

### PART 3: APPLICATION NAVIGATION & ROUTE GUARDS

| Test ID | Route Tested | User Role | Expected Behavior | Actual Behavior | Status |
|---|---|---|---|---|:---:|
| **TC-NAV01** | `/inventory` | Standard User | Catalog table view renders | Inventory page loaded with items | **PASS** |
| **TC-NAV02** | `/transactions` | Standard User | Circular transactions ledger renders | Transactions ledger table visible | **PASS** |
| **TC-NAV03** | `/ai-predictions` | Standard User | AI Decision Engine view renders | AI upload and classifier interface visible | **PASS** |
| **TC-NAV04** | `/impact-passports` | Standard User | Digital Product Passport page renders | Impact passports grid loaded | **PASS** |
| **TC-NAV05** | `/pickup-partners` | Standard User | Partner Network Finder renders | Map and partner listing visible | **PASS** |
| **TC-NAV06** | `/repair-guide` | Standard User | Repair Tutorials view renders | Circular repair guides rendered | **PASS** |
| **TC-NAV07** | `/rewards-store` | Standard User | EcoCredits store renders | Rewards and eco-token catalog visible | **PASS** |
| **TC-NAV08** | `/reports` | Standard User | ESG Analytics and reports render | Reports and chart components loaded | **PASS** |
| **TC-NAV09** | `/admin-dashboard` | Administrator | System Admin console renders | Admin metrics and management console loaded | **PASS** |
| **TC-NAV10** | `/inventory` (Guarded) | Unauthenticated | Direct access redirected to `/login` | Intercepted by ProtectedRoute; redirected to `/login` | **PASS** |

---

## 4. How to Re-Run the Test Suite

### Step 1: Ensure Application Servers Are Running
```bash
# Terminal 1: Backend API (FastAPI)
cd /Users/akashreddy/Desktop/SE/backend
source venv/bin/activate
uvicorn app.main:app --port 8000

# Terminal 2: Frontend App (React / Vite)
cd /Users/akashreddy/Desktop/SE/frontend
npm run dev
```

### Step 2: Execute the Automated Selenium Suite
From the project root:
```bash
cd /Users/akashreddy/Desktop/SE

# Run all 52 tests in headless Chrome and generate the visual HTML report:
./backend/venv/bin/pytest tests/ \
  --base-url=http://localhost:5173 \
  --html=tests/report.html \
  --self-contained-html -v
```

### Step 3: Run in Visible (Headed) Mode *(Watch Chrome Automate Live)*
To demonstrate the live automation to your faculty on screen:
```bash
./backend/venv/bin/pytest tests/test_ai_classification.py --headed -v
```

### Step 4: Open the Interactive HTML Report
```bash
open tests/report.html
```

---

## 5. Concise Explanation for Faculty Presentation

When presenting this testing implementation to your faculty or evaluator, you can explain:

1. **Automation Architecture**:
   > *"We developed an end-to-end testing suite using Selenium WebDriver and Pytest in Python. Rather than using mock UI drivers, Selenium automates a real Google Chrome browser instance to simulate authentic user workflows, validate DOM states, and verify client-side validation logic."*
2. **Functional Testing Rigor**:
   > *"For functional testing, we applied **Equivalence Partitioning** and **Boundary Value Analysis**. In Scenario 1, we tested valid user registrations, duplicate prevention, role-based redirection across standard users and administrators, and route guards. In Scenario 2, we tested our multi-model AI decision engine by uploading real circular economy dataset images, verifying multi-phase classification progress spinners, extracting primary predicted material classes, and validating confidence score badges."*
3. **Non-Functional Testing Rigor**:
   > *"For non-functional testing, we evaluated browser performance by interfacing directly with the browser's native **W3C Navigation Timing API** to record DNS, DOMContentLoaded, and window load latency. We also tested cross-device responsive layout fidelity by programmatically resizing the browser window across mobile (375px), tablet (768px), and desktop (1920px) viewports to verify that no horizontal overflow or clipping occurs."*
4. **Outcome & Verification**:
   > *"All 52 test cases executed cleanly in ~74 seconds with a 100% pass rate. An interactive HTML execution report with pass/fail metrics was automatically generated at `tests/report.html`."*
