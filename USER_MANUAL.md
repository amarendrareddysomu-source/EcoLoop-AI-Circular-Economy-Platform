# User Operational Manual & User Guide

**Platform**: AI-Powered Circular Economy Action Decision Support Platform  
**Version**: 2.0.0 (Production Release)  

---

## 1. Introduction

Welcome to the **AI-Powered Circular Economy Action Decision Support Platform**! This user guide provides step-by-step instructions for operating the web platform across all 5 user roles: **Guest**, **Registered User**, **NGO Representative**, **Recycling Center Operator**, and **System Administrator**.

---

## 2. User Account Management

### 2.1 Registration
1. Navigate to `http://localhost:5173/register` (or platform domain).
2. Enter your **Full Name**, **Email Address**, and a secure **Password** (minimum 8 characters).
3. Select your user role:
   - **General User**: For individuals listing used items.
   - **NGO Representative**: For community organizations accepting donations.
   - **Recycling Facility**: For industrial recyclers accepting raw materials.
4. Click **Register Account**.

```text
┌────────────────────────────────────────────────────────┐
│                   Create an Account                    │
│                                                        │
│ Full Name:     [ Jane Doe                            ] │
│ Email Address: [ jane@example.com                    ] │
│ Password:      [ ••••••••••••                        ] │
│ Account Role:  (o) User  ( ) NGO  ( ) Recycling Center │
│                                                        │
│                  [ REGISTER ACCOUNT ]                  │
└────────────────────────────────────────────────────────┘
```

### 2.2 Logging In
1. Navigate to `/login`.
2. Enter registered credentials.
3. Upon authentication, a secure Bearer JWT token is issued, redirecting you to your designated dashboard portal.

---

## 3. Image-Based AI Pipeline & Evaluation

### 3.1 Uploading an Item Image
1. Navigate to **AI Intelligence** from the navigation sidebar.
2. Drag and drop or browse to select an item image (`.jpg`, `.jpeg`, `.png`, `.webp`, maximum 10MB).
3. Review the image preview and file size details.
4. Click **Analyze Image with AI** to execute the end-to-end computer vision and circular intelligence pipeline.

```text
┌────────────────────────────────────────────────────────┐
│             Upload Item Image for AI Pipeline          │
│                                                        │
│ [ Drag and Drop Image File Here (JPG/PNG/WEBP <10MB) ] │
│                                                        │
│ [ Image Preview: laptop.jpg (1.85 MB) ]                │
│                                                        │
│               [ ANALYZE IMAGE WITH AI ]                │
└────────────────────────────────────────────────────────┘
```

### 3.2 Automated Image Validation & Preprocessing
The platform automatically validates and prepares uploaded images:
- **Validation**: Checks MIME type, file extension, magic bytes header, maximum 10MB size limit, and structural image integrity. Unsupported or corrupted files are rejected with clear error feedback.
- **Preprocessing**: Performs automated RGB color conversion, 224x224 dimension resizing, Gaussian noise reduction filtering, and pixel value normalization.

### 3.3 Reviewing AI Analysis Results & Actions
Upon clicking **Analyze Image with AI**, the AI Pipeline processes the image and returns comprehensive metrics:

- **Predicted Category**: Object classification (e.g., *Electronics*, confidence 94%).
- **Condition Assessment**: Evaluated wear rating (e.g., *Good*).
- **Repairability Score**: Component repair index gauge (e.g., *85/100*).
- **Sustainability Score**: Environmental impact score (e.g., *92/100*), featuring exact CO₂ saved (*46.25 kg*) and landfill diverted (*2.50 kg*).
- **Estimated Resale Price**: Residual market value prediction (e.g., *$450.00*).
- **Circular Action Recommendation**: Disposition action (**Sell**, **Donate**, **Repair**, **Reuse**, or **Recycle**) with automated strategic reasoning.

#### Post-Prediction Actions
- **Save to Inventory**: Click **Save to Inventory** to automatically persist the classified item into your personal inventory with image URL and sustainability metrics.
- **Create Listing / Sell**: Click **Create Listing / Sell** to pre-fill item attributes into a transaction listing.

---

## 4. Personal Inventory & Transaction Processing

### 4.1 Managing Inventory
Navigate to `/inventory` to view your active item catalog:
- Filter by status (**Available**, **Reserved**, **Completed**).
- Filter by category or AI recommendation type.
- Click on any item card to view complete AI analysis logs and environmental impact metrics.

### 4.2 Initiating a Transaction / Handoff
1. Browse available platform items.
2. Click **Initiate Handoff** or **Claim Item**.
3. Select transaction path (**Donate to NGO**, **Sell to Buyer**, **Send to Recycling Queue**).
4. Enter pickup/dropoff notes.
5. The state machine transitions the item status from `available` to `reserved` and alerts the counterparty.

---

## 5. Role-Specific Portals

### 5.1 NGO Portal (`/ngo-dashboard`)
- View incoming community donation claims.
- Accept or approve donation requests.
- Track monthly received weight (kg) against organizational capacity limit.

### 5.2 Recycling Center Portal (`/recycling-dashboard`)
- View recyclable material intake queue filtered by categories (Electronics, Plastic, Paper, Metal, Glass, Appliances).
- Update material processing stage (**Received**, **In-Processing**, **Recycled**).
- Monitor diverted tonnage metrics.

### 5.3 System Admin Dashboard (`/admin-dashboard`)
- Real-time platform impact statistics (Total Items, CO₂ Saved, Landfill Weight Diverted).
- Manage user directory (Activate, Deactivate, Modify Role).
- Monitor AI decision logs and system health diagnostics.

---

## 6. Notifications & Theme Preferences

- **In-App Notifications**: Click the bell icon in the header navigation to view real-time notifications for transaction status changes and donation claims.
- **Theme Toggle**: Click the Sun/Moon icon in the navigation bar to switch between Light Mode and Dark Glassmorphic Mode.
