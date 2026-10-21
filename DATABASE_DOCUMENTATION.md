# Database Schema Specification & Documentation

**Platform**: AI-Powered Circular Economy Action Decision Support Platform  
**Database Engines Supported**: PostgreSQL 15 (Production) / SQLite 3 (Development/Testing)  
**ORM Framework**: SQLAlchemy 2.0.28 with Alembic Migrations  

---

## 1. Relational Schema Architecture

The database follows **3rd Normal Form (3NF)** rules to eliminate redundancy, ensure domain integrity, and maintain data consistency across multi-role transactions:

```text
  +------------------+         +---------------------+
  |      USERS       |1       1|    ORGANIZATIONS    |
  |------------------|---------|---------------------|
  | id (PK)          |         | id (PK)             |
  | email (UK)       |         | user_id (FK, UK)    |
  | role             |         | org_type            |
  | organization_id  |-------->| name                |
  +--------+---------+         +---------------------+
           |1
           |
           |0..*
  +--------v---------+         +---------------------+
  |      ITEMS       |1       *|    TRANSACTIONS     |
  |------------------|---------|---------------------|
  | id (PK)          |         | id (PK)             |
  | user_id (FK)     |         | item_id (FK)        |
  | title            |         | sender_id (FK)      |
  | category         |         | recipient_id (FK)   |
  | condition        |         | status              |
  +------------------+         +---------------------+
```

---

## 2. Table Specifications

### 2.1 Table: `users`
Stores user authentication credentials, assigned roles, and profile settings.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key, Auto-increment | Unique user identifier |
| `email` | `VARCHAR` | Unique, Not Null, Indexed | User login email address |
| `hashed_password` | `VARCHAR` | Not Null | Bcrypt password hash |
| `full_name` | `VARCHAR` | Not Null | Full display name |
| `role` | `VARCHAR` | Not Null, Default: `'user'`, Indexed | Role enum (`user`, `ngo`, `recycling_center`, `admin`, `super_admin`) |
| `organization_id` | `INTEGER` | Foreign Key (`organizations.id`, SET NULL), Indexed | Reference to affiliated organization |
| `is_active` | `BOOLEAN` | Default: `TRUE`, Indexed | Account active status |
| `is_verified` | `BOOLEAN` | Default: `FALSE` | Email verification flag |
| `verification_token`| `VARCHAR` | Nullable, Indexed | Email verification token |
| `reset_token` | `VARCHAR` | Nullable, Indexed | Password reset token |
| `refresh_token` | `VARCHAR` | Nullable | Active JWT refresh token hash |
| `location` | `VARCHAR` | Nullable | Geographic location string |
| `created_at` | `TIMESTAMP` | Default: `CURRENT_TIMESTAMP`, Indexed | Account registration timestamp |
| `updated_at` | `TIMESTAMP` | Nullable, On Update | Last modification timestamp |

### 2.2 Table: `organizations`
Stores profiles for registered Non-Governmental Organizations (NGOs) and Recycling Centers.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key, Auto-increment | Unique organization identifier |
| `user_id` | `INTEGER` | Foreign Key (`users.id`, CASCADE), Unique, Indexed | Account owner user ID |
| `name` | `VARCHAR` | Not Null, Indexed | Legal organization name |
| `org_type` | `VARCHAR` | Not Null, Indexed | Organization type (`ngo`, `recycling_center`) |
| `description` | `TEXT` | Nullable | Operational description |
| `address` | `VARCHAR` | Not Null | Physical street address |
| `phone` | `VARCHAR` | Not Null | Contact phone number |
| `capacity_kg_per_month`| `INTEGER`| Default: `1000` | Material handling capacity (kg/month) |
| `accepted_categories` | `VARCHAR` | Not Null | Comma-separated category whitelist |
| `is_verified` | `BOOLEAN` | Default: `TRUE` | Verification approval flag |
| `created_at` | `TIMESTAMP` | Default: `CURRENT_TIMESTAMP` | Profile creation timestamp |

### 2.3 Table: `items`
Central catalog storing user-uploaded items, AI predictions, and lifecycle states.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key, Auto-increment | Unique item identifier |
| `user_id` | `INTEGER` | Foreign Key (`users.id`, CASCADE), Indexed | Item owner user ID |
| `title` | `VARCHAR` | Not Null, Indexed | Item title / description |
| `category` | `VARCHAR` | Not Null, Indexed | Predicted category (Electronics, Furniture, etc.) |
| `condition` | `VARCHAR` | Not Null, Indexed | Condition rating (Excellent, Good, Fair, Poor) |
| `age_years` | `FLOAT` | Default: `1.0` | Item age in years |
| `usage_level` | `VARCHAR` | Default: `'Moderate'` | Usage intensity profile |
| `original_price` | `FLOAT` | Default: `0.0` | Original retail price ($) |
| `predicted_price` | `FLOAT` | Default: `0.0`, Indexed | AI predicted resale value ($) |
| `co2_saved_kg` | `FLOAT` | Default: `0.0` | Calculated carbon offset (kg) |
| `waste_diverted_kg`| `FLOAT` | Default: `0.0` | Calculated landfill diversion (kg) |
| `recommended_action`| `VARCHAR` | Not Null, Indexed | AI recommendation (Sell, Donate, Repair, Reuse, Recycle) |
| `image_url` | `VARCHAR` | Nullable | Static upload image URL |
| `status` | `VARCHAR` | Default: `'available'`, Indexed | Lifecycle status (`available`, `reserved`, `completed`) |
| `created_at` | `TIMESTAMP` | Default: `CURRENT_TIMESTAMP`, Indexed | Upload timestamp |

### 2.4 Table: `transactions`
State machine managing circular material handoffs.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key, Auto-increment | Unique transaction identifier |
| `item_id` | `INTEGER` | Foreign Key (`items.id`, CASCADE), Indexed | Subject item ID |
| `sender_id` | `INTEGER` | Foreign Key (`users.id`, CASCADE), Indexed | Item owner user ID |
| `recipient_id` | `INTEGER` | Foreign Key (`users.id`, CASCADE), Indexed | Claiming user / NGO / Recycler ID |
| `transaction_type` | `VARCHAR` | Not Null, Indexed | Transfer type (Donate, Sell, Recycle, Repair) |
| `status` | `VARCHAR` | Default: `'pending'`, Indexed | State (`pending`, `approved`, `in_transit`, `completed`, `cancelled`) |
| `notes` | `TEXT` | Nullable | Transaction notes / pickup instructions |
| `created_at` | `TIMESTAMP` | Default: `CURRENT_TIMESTAMP`, Indexed | Creation timestamp |

### 2.5 Table: `notifications`
In-app user notification log.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key, Auto-increment | Unique notification ID |
| `user_id` | `INTEGER` | Foreign Key (`users.id`, CASCADE), Indexed | Recipient user ID |
| `title` | `VARCHAR` | Not Null | Short notification title |
| `message` | `TEXT` | Not Null | Full notification message |
| `is_read` | `BOOLEAN` | Default: `FALSE`, Indexed | Read status flag |
| `created_at` | `TIMESTAMP` | Default: `CURRENT_TIMESTAMP`, Indexed | Timestamp |

---

## 3. Foreign Key Cyclic Dependency Resolution

To prevent circular dependency locks during table drops and schema migrations between `users.organization_id` and `organizations.user_id`, SQLAlchemy definitions enforce `use_alter=True`:

```python
# User Model
organization_id = Column(
    Integer, 
    ForeignKey("organizations.id", ondelete="SET NULL", use_alter=True, name="fk_users_organization_id"), 
    nullable=True, 
    index=True
)

# Organization Model
user_id = Column(
    Integer, 
    ForeignKey("users.id", ondelete="CASCADE", use_alter=True, name="fk_organizations_user_id"), 
    unique=True, 
    nullable=False, 
    index=True
)
```

---

## 4. Indexing Strategy

Indexes are applied to high-cardinality foreign keys, search filters, and sort columns:

1. **Primary Lookup Indexes**: `users.email`, `users.role`, `organizations.org_type`, `items.category`, `items.status`.
2. **Foreign Key Indexes**: `users.organization_id`, `organizations.user_id`, `items.user_id`, `transactions.item_id`, `transactions.sender_id`, `transactions.recipient_id`, `notifications.user_id`.
3. **Analytics & Timestamp Indexes**: `users.created_at`, `items.created_at`, `transactions.created_at`, `notifications.created_at`.
