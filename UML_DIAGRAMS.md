# System UML Diagrams Specification

**Platform**: AI-Powered Circular Economy Action Decision Support Platform  
**Documentation Purpose**: Complete UML Architectural & Behavioral Diagrams  

---

## 1. System Architecture Diagram

```mermaid
graph TD
    UserClient[Web Browser / Mobile Client] -->|HTTP/HTTPS Port 80/443| NginxProxy[Nginx Edge Reverse Proxy]
    
    subgraph Container Cluster (Docker Compose)
        NginxProxy -->|/| FrontendApp[Frontend Container - Nginx Static SPA]
        NginxProxy -->|/api/v1| BackendAPI[Backend Container - FastAPI]
        
        subgraph FastAPI Backend Application
            BackendAPI --> AuthDep[JWT Auth & RBAC Middleware]
            AuthDep --> Controllers[API Route Endpoints]
            Controllers --> Services[Business Service Layer]
            Services --> Repositories[SQLAlchemy Repository Layer]
            Services --> AIEngine[AI Multimodal Decision Engine]
        end
        
        subgraph Multi-Model AI Engine
            AIEngine --> EfficientNet[EfficientNet-B0 Classifier]
            AIEngine --> CondEstimator[Condition & Wear Predictor]
            AIEngine --> RandomForest[Random Forest Price Regressor]
            AIEngine --> ImpactCalc[Sustainability Calculator]
            AIEngine --> RecStrategy[Strategy Recommendation Engine]
        end
        
        Repositories --> Database[(PostgreSQL 15 Container)]
    end
```

---

## 2. Use Case Diagram

```mermaid
graph LR
    subgraph Actors
        Guest([Guest User])
        User([Registered User])
        NGO([NGO Representative])
        Recycler([Recycling Center Operator])
        Admin([System Admin])
    end

    subgraph Platform Use Cases
        UC1(Browse Public Items & Impact Stats)
        UC2(User Registration & JWT Login)
        UC3(Upload Item Image & Trigger AI Evaluation)
        UC4(View AI Condition, Price & Recommendations)
        UC5(Create Inventory Listing)
        UC6(Initiate Item Transaction / Claim)
        UC7(Accept Donation Claim)
        UC8(Accept Recyclable Material Queue)
        UC9(Update Processing Status)
        UC10(View Platform Analytics & Reports)
        UC11(Manage Users & System Logs)
    end

    Guest --> UC1
    Guest --> UC2
    
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    
    NGO --> UC7
    NGO --> UC10
    
    Recycler --> UC8
    Recycler --> UC9
    Recycler --> UC10
    
    Admin --> UC10
    Admin --> UC11
```

---

## 3. Activity Diagram (Item Upload to Disposition Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> UploadImage: User Uploads Item Image
    UploadImage --> ValidateFile: Check Extension, MIME, Size & Magic Bytes
    
    state ValidationCheck <<choice>>
    ValidateFile --> ValidationCheck
    ValidationCheck --> RejectFile: Invalid File (Spoofed MIME/Magic Byte Failure)
    RejectFile --> [*]
    
    ValidationCheck --> RunAIClassifier: Valid File
    RunAIClassifier --> ExtractFeatures: EfficientNet-B0 Category Prediction
    ExtractFeatures --> ConditionEvaluation: Condition & Wear Score Calculation
    ConditionEvaluation --> PricePrediction: Random Forest Resale Price Model
    PricePrediction --> SustainabilityMath: CO2 & Landfill Diversion Calculation
    SustainabilityMath --> StrategyRecommendation: Strategy Pattern Action Selection
    
    StrategyRecommendation --> DisplayResults: Present AI Findings to User
    DisplayResults --> SaveToInventory: Confirm & Save to Platform Inventory
    
    SaveToInventory --> MatchEngine: Route to NGO / Recycler Queue
    MatchEngine --> CreateTransaction: User/Org Initiates Transfer
    CreateTransaction --> CompleteTransaction: Item Processing Completed
    CompleteTransaction --> [*]
```

---

## 4. Sequence Diagram (Image-Based AI Pipeline)

```mermaid
sequenceDiagram
    autonumber
    actor User as User Browser
    participant API as FastAPI Endpoint (/ai/classify-image)
    participant Upload as Upload Service
    participant AI as AI Engine Pipeline
    participant DB as Database / AILog

    User->>API: POST /api/v1/ai/classify-image (UploadFile image)
    API->>Upload: validate_image(file, file_bytes) (MIME, Magic Bytes, Size, Integrity)
    Upload-->>API: Extension Validated & File Saved (/static/uploads/uuid.jpg)
    
    API->>AI: Image Preprocessing (224x224 Resize, RGB, Denoise, Normalization)
    
    API->>AI: image_classifier.classify_image(file_bytes)
    AI-->>API: Category: "Electronics", Confidence: 0.94
    
    API->>AI: condition_predictor.predict_condition(file_bytes)
    AI-->>API: Condition: "Good", Wear Score: 18.5
    
    API->>AI: Compute Repairability & Sustainability Score
    AI-->>API: Repairability: 85/100, Sustainability: 92/100 (CO2: 46.25kg)
    
    API->>AI: price_predictor.predict_price(...)
    AI-->>API: Resale Price: $450.00
    
    API->>AI: recommendation_engine.get_recommendation(...)
    AI-->>API: Action: "Sell", Reasoning: "High resale demand ($450.00)"
    
    API->>DB: Log Inference to AILog Table
    DB-->>API: Log Persisted
    
    API-->>User: HTTP 200 OK (ImageClassificationResponse Payload)
```

---

## 5. Class Diagram (Core Backend Domain & AI Architecture)

```mermaid
classDiagram
    class Base {
        +Integer id
        +DateTime created_at
    }

    class User {
        +String email
        +String hashed_password
        +String full_name
        +String role
        +Integer organization_id
        +Boolean is_active
        +Boolean is_verified
        +verify_password(plain)
    }

    class Organization {
        +Integer user_id
        +String name
        +String org_type
        +String address
        +Integer capacity_kg_per_month
    }

    class Item {
        +Integer user_id
        +String title
        +String category
        +String condition
        +Float predicted_price
        +Float co2_saved_kg
        +Float waste_diverted_kg
        +String recommended_action
        +String status
    }

    class Transaction {
        +Integer item_id
        +Integer sender_id
        +Integer recipient_id
        +String transaction_type
        +String status
    }

    class ImageClassifier {
        +Model model
        +classify_image(bytes) Dict
    }

    class PricePredictor {
        +Pipeline pipeline
        +predict_price(cat, brand, age, cond, orig_price) Float
    }

    class RecommendationEngine {
        +RecommendationStrategy strategy
        +get_recommendation(cat, cond, age, price) Dict
    }

    Base <|-- User
    Base <|-- Organization
    Base <|-- Item
    Base <|-- Transaction
    User "1" <-- "0..1" Organization : owns
    User "1" --> "0..*" Item : posts
    Item "1" --> "0..*" Transaction : linked
```

---

## 6. Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USERS ||--o| ORGANIZATIONS : "manages"
    USERS ||--o{ ITEMS : "owns"
    USERS ||--o{ TRANSACTIONS : "initiates"
    USERS ||--o{ NOTIFICATIONS : "receives"
    ITEMS ||--o{ TRANSACTIONS : "subject_of"

    USERS {
        int id PK
        string email UK
        string hashed_password
        string full_name
        string role
        int organization_id FK
        boolean is_active
        datetime created_at
    }

    ORGANIZATIONS {
        int id PK
        int user_id FK,UK
        string name
        string org_type
        string address
        int capacity_kg_per_month
    }

    ITEMS {
        int id PK
        int user_id FK
        string title
        string category
        string condition
        float predicted_price
        float co2_saved_kg
        float waste_diverted_kg
        string recommended_action
        string status
        datetime created_at
    }

    TRANSACTIONS {
        int id PK
        int item_id FK
        int sender_id FK
        int recipient_id FK
        string transaction_type
        string status
        datetime created_at
    }

    NOTIFICATIONS {
        int id PK
        int user_id FK
        string title
        string message
        boolean is_read
        datetime created_at
    }
```

---

## 7. Deployment Diagram

```mermaid
graph TB
    subgraph Client Environment
        Browser[Web Browser / Client Device]
    end

    subgraph Production Cloud Instance / Server
        subgraph Nginx Edge Proxy (Port 80/443)
            Proxy[Nginx Reverse Proxy & SSL Termination]
        end

        subgraph Docker Bridge Network
            FrontendContainer[Frontend Nginx SPA Container - Port 80]
            BackendContainer[FastAPI Backend Container - Port 8000]
            PostgresContainer[PostgreSQL 15 Container - Port 5432]
        end

        subgraph Persistent Volumes
            PostgresData[(postgres_data Volume)]
            UploadsData[(uploads_data Volume)]
        end
    end

    Browser -->|HTTPS| Proxy
    Proxy -->|Proxy /| FrontendContainer
    Proxy -->|Proxy /api/v1| BackendContainer
    BackendContainer -->|SQL Connection| PostgresContainer
    PostgresContainer --> PostgresData
    BackendContainer --> UploadsData
```

---

## 8. System Component Diagram

```mermaid
graph LR
    subgraph Frontend Subsystem
        UI[React 18 SPA Components]
        Router[AppRoutes & ProtectedRoute]
        Context[Auth & Theme Contexts]
        UI --> Router
        Router --> Context
    end

    subgraph Backend Subsystem
        API[FastAPI Controllers]
        Security[JWT & Security Middleware]
        Services[Business Logic Services]
        Repos[SQLAlchemy Repositories]
        API --> Security
        Security --> Services
        Services --> Repos
    end

    subgraph AI Subsystem
        CV[EfficientNet Classifier]
        RF[Random Forest Pricing]
        Rules[Strategy Recommender]
    end

    subgraph Database Subsystem
        DB[(PostgreSQL 15)]
    end

    Context -->|HTTP REST| API
    Services --> CV
    Services --> RF
    Services --> Rules
    Repos --> DB
```
