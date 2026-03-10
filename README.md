# Field2Site: Tractor & Equipment Rental System

Field2Site is a full-stack digital marketplace connecting **Hosts** (equipment owners) with **Buyers** (farmers and construction contractors). It solves the problem of high capital expenditure in agriculture and construction by enabling a "sharing economy" for heavy machinery.

---

## 🏗️ System Architecture

The project follows a **Decoupled Client-Server Architecture**, with a React SPA frontend communicating with an Express REST API that queries a MySQL database.

```
graph TD
    Client[React + Vite Frontend :5173]
    Server[Express Node.js Backend :5000]
    DB[(MySQL Database – rental_system)]
    Email[SMTP / Gmail – Nodemailer]
    Uploads[Local Disk – server/uploads/]

    Client -- REST API / axios --> Server
    Server -- SQL Queries --> DB
    Server -- OTP Emails --> Email
    Server -- Multer FS Stream --> Uploads
    DB -- Result Sets --> Server
    Server -- JSON Responses --> Client
```

### 💻 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite, React Router v7, Tailwind CSS v4 |
| Animations | Framer Motion, @react-spring/web |
| Icons | Lucide React |
| HTTP Client | Axios |
| Backend | Node.js, Express 5 |
| Database | MySQL 2 (mysql2/promise) with Connection Pool |
| File Uploads | Multer (disk storage, 5 MB limit) |
| Email / OTP | Nodemailer (SMTP / Gmail App Password) |
| Environment | dotenv |

---

## 📊 Database Schema

Database: `rental_system` — designed in **3rd Normal Form (3NF)** with strict integrity constraints.

### Tables

| Table | Description |
|---|---|
| `HOST` | Equipment owners (Individual / Enterprise) |
| `BUYER` | Renters — Farm or Construction type |
| `FARM_EQUIPMENT` | Farm machinery listings (linked to a Host) |
| `CONSTRUCTION_EQUIPMENT` | Construction machinery listings (linked to a Host) |
| `BOOKING` | Rental transactions linking Buyer ↔ Host ↔ Equipment |
| `PAYMENT` | Payment records per booking (Cash, Card, UPI, Net Banking, Wallet) |
| `REVIEW` | Buyer reviews per booking; auto-updates `HOST.Rating` |
| `MAINTENANCE` | Service log for any equipment |

### Entity-Relationship Diagram (ERD)
```mermaid
erDiagram
    HOST ||--o{ FARM_EQUIPMENT : owns
    HOST ||--o{ CONSTRUCTION_EQUIPMENT : owns
    BUYER ||--o{ BOOKING : makes
    HOST ||--o{ BOOKING : receives
    BOOKING ||--|| PAYMENT : triggers
    BOOKING ||--o{ REVIEW : receives
    FARM_EQUIPMENT ||--o{ MAINTENANCE : "tracked"
    CONSTRUCTION_EQUIPMENT ||--o{ MAINTENANCE : "tracked"

    HOST {
        int Host_ID PK
        string Host_Name
        string Host_Type "Individual/Enterprise"
        string Email UNIQUE
        decimal Rating
        boolean Verified_Status
    }
    BUYER {
        int Buyer_ID PK
        string Name
        enum Buyer_Type "Farm/Construction"
        string Email UNIQUE
    }
    BOOKING {
        int Booking_ID PK
        int Buyer_ID FK
        int Host_ID FK
        int Equipment_ID
        enum Equipment_Type "Farm/Construction"
        enum Usage_Type "Hourly/Daily"
        decimal Total_Amount
        enum Status "Pending/Confirmed/Completed/Cancelled"
    }
    PAYMENT {
        int Payment_ID PK
        int Booking_ID FK
        decimal Amount
        enum Mode "Cash/Card/UPI/Net Banking/Wallet"
        enum Status "Pending/Completed/Failed/Refunded"
    }
```

### Key Design Decisions
- **`ON DELETE CASCADE`** on all FK relationships — deleting a Host removes their equipment, bookings, and reviews.
- **`ENUM` columns** for `Availability_Status`, `Status`, `Mode`, etc. — prevents invalid data entry.
- **Performance indexes** on `Host_ID`, `Buyer_ID`, `Status`, `Start_Date/End_Date` and `Payment_Status`.
- **`Image_URL VARCHAR(500)`** on equipment tables — only the filename is stored; files live in `server/uploads/`.
- **Atomic booking transaction** — creating a booking also sets `Availability_Status = 'Rented'` inside a single DB transaction (rolls back on failure).
- **Background task** — a `setInterval` runs every minute to auto-complete expired bookings and restore equipment availability.

---

## 🖥️ Frontend Pages & Components

| Route | Page | Access |
|---|---|---|
| `/` | Home — hero + category landing | Public |
| `/browse` | Browse — filterable equipment grid | Public |
| `/equipment/:type/:id` | Equipment Detail — full info + booking flow | Public (booking requires login) |
| `/login` | Login — email-based, OTP verified | Public |
| `/signup` | Sign Up — multi-step: role → details → OTP | Public |
| `/dashboard` | Dashboard — buyer stats, active rentals, order history | Buyer |
| `/listings` | Listings — host equipment CRUD + booking management | Host |
| `/payment` | Payment — booking confirmation + payment mode | Protected (Buyer) |

### Reusable Components
- `Navbar` — context-aware top bar
- `SideNav` — dashboard/listings sidebar
- `EquipmentFilters` — category/status/price filter bar
- `EquipmentToggle` — farm ↔ construction tab switch
- `ProtectedRoute` — redirects unauthenticated users to `/login`

### Context
- `AuthContext` — persists logged-in user to `localStorage`; provides `login`, `logout`, `user`
- `EquipmentContext` — shared equipment type state across Browse and Detail pages

---

## 🔌 API Endpoints

### Authentication (`/api/auth`)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/check-email` | Proactive duplicate check before OTP is sent |
| POST | `/send-otp` | Generates 4-digit OTP (10 min TTL), sends email |
| POST | `/verify-otp` | Validates OTP against server-side `Map` |
| POST | `/signup` | Creates Buyer or Host record in DB |
| POST | `/login` | Email-based login; returns full user profile |

### Equipment (`/api/equipment`)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/:type` | List all equipment (farm/construction) with host info |
| GET | `/:type/:id` | Single equipment detail |
| POST | `/:type` | Add equipment (multipart/form-data with image) |
| PUT | `/:type/:id` | Update equipment (optional new image) |
| DELETE | `/:type/:id` | Delete equipment |
| PATCH | `/:type/:id/toggle-status` | Toggle Available ↔ Rented |

### Host
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/host-equipment/:hostId` | All equipment owned by host |
| GET | `/api/host/stats/:hostId` | Equipment count, rented count, earnings, avg rating |
| GET | `/api/buyer/stats/:buyerId` | Active rentals & total order count |

### Bookings (`/api/bookings`)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/` | Create booking + mark equipment as Rented (transaction) |
| GET | `/buyer/:id` | All bookings for a buyer |
| GET | `/host/:id` | All bookings received by a host |
| PUT | `/:id/status` | Update status; restores availability on Completed/Cancelled |

### Payments & Reviews
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/payments` | Record payment for a booking |
| GET | `/api/payments/booking/:id` | Get payment by booking |
| POST | `/api/reviews` | Submit review; auto-updates host avg rating |
| GET | `/api/reviews/host/:id` | All reviews for a host |

---

## 🔒 Security & Edge Case Handling

### Duplicate Signup
Two-layer prevention:
1. **Proactive**: `POST /api/auth/check-email` is called on blur before sending OTP.
2. **Reactive**: MySQL `UNIQUE` constraint on `Email` as the final guard — returns `ER_DUP_ENTRY` → 409.

### OTP Security
- 4-digit OTP stored server-side in a `Map` with a 10-minute expiration timestamp.
- Verification checks both value equality **and** `Date.now() < expires`.
- OTP entry is deleted after expiry to prevent reuse.

### Role-Based Access Control (RBAC)
- `AuthContext` stores `user.type` (`buyer` / `host`).
- `ProtectedRoute` wraps the Payment page — unauthenticated users are redirected to `/login`.
- Dashboard and Listings pages use `useEffect` guards to redirect wrong-role users.

### Image Uploads
- Multer validates MIME type + extension (jpeg, jpg, png, gif, webp) and enforces a **5 MB** size limit.
- Files are served as static assets from `/uploads/*`.

---

## 🚀 Getting Started

### Prerequisites
- Node.js ≥ 18
- MySQL ≥ 8
- Python 3 + `mysql-connector-python` (for dataset seeding)
- A Gmail account with an **App Password** enabled

### 1. Clone & Install
```bash
git clone <repo-url>
cd dbms
npm install
```

### 2. Create the Database
```bash
# Option A – fresh setup via Python (creates DB + tables + seed data)
python setup_database.py

# Option B – SQL only
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS rental_system;"
mysql -u root -p rental_system < create_tables.sql
```

### 3. Configure Environment
Create `server/.env` (use `server/.env.example` as a template):
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=rental_system
PORT=5000

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASS=your_gmail_app_password
EMAIL_FROM=your_gmail@gmail.com
```

### 4. Start the Backend
```bash
node server/server.js
# Server starts at http://localhost:5000
```

### 5. Start the Frontend
```bash
npm run dev
# Frontend starts at http://localhost:5173
```

---

## 📁 Project Structure

```
dbms/
├── server/
│   ├── server.js            # Express REST API (all routes)
│   ├── .env                 # DB + Email credentials (gitignored)
│   ├── .env.example         # Template for .env
│   └── uploads/             # Equipment image storage (auto-created)
├── src/
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Browse.jsx
│   │   ├── EquipmentDetail.jsx
│   │   ├── Login.jsx
│   │   ├── SignUp.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Listings.jsx
│   │   └── Payment.jsx
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── SideNav.jsx
│   │   ├── EquipmentFilters.jsx
│   │   ├── EquipmentToggle.jsx
│   │   └── ProtectedRoute.jsx
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   └── EquipmentContext.jsx
│   ├── services/            # Axios API client
│   └── lib/                 # Utility helpers
├── create_tables.sql        # Full DB schema
├── setup_database.py        # DB creation + seeding script
├── add_image_column.sql     # Migration for image columns
├── dataset.py               # Seed data generator
├── package.json
└── vite.config.js
```

---

