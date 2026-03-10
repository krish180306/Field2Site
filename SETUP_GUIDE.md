# Database Connection Setup Guide

## ✅ Completed Steps

1. **Added Image Support to Equipment Tables**
   - Added `Image_URL VARCHAR(500)` column to FARM_EQUIPMENT table
   - Added `Image_URL VARCHAR(500)` column to CONSTRUCTION_EQUIPMENT table
   - Updated both `create_tables.sql` and `setup_database.py`

2. **Created Backend API Server**
   - Express.js server with MySQL connection
   - Multer middleware for image uploads
   - REST API endpoints for all operations

3. **Created API Service Layer**
   - Centralized axios-based API client
   - Error handling and interceptors

4. **Updated Frontend Context**
   - AuthContext now uses backend API
   - localStorage persistence for user sessions

## 📋 Next Steps to Complete Setup

### 1. Set Up Database Credentials

Edit `server/.env` file with your MySQL credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=rental_system
PORT=5000
```

### 2. Create/Update Database

**Option A: New Database**
```bash
python setup_database.py
```

**Option B: Add Image Column to Existing Database**
```bash
mysql -u root -p rental_system < add_image_column.sql
```

### 3. Start Backend Server

```bash
cd server
node server.js
```

The server will run on http://localhost:5000

### 4. Start Frontend (Already Running)

Your frontend is already running on http://localhost:5173

## 🔌 API Endpoints Available

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user

### Equipment
- `GET /api/equipment/:type` - Get all equipment (farm/construction)
- `GET /api/equipment/:type/:id` - Get specific equipment
- `POST /api/equipment/:type` - Add equipment (with image upload)
- `PUT /api/equipment/:type/:id` - Update equipment
- `DELETE /api/equipment/:type/:id` - Delete equipment
- `GET /api/equipment/host/:hostId` - Get host's equipment

### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings/buyer/:id` - Get buyer bookings
- `GET /api/bookings/host/:id` - Get host bookings
- `PUT /api/bookings/:id/status` - Update booking status

### Payments
- `POST /api/payments` - Create payment
- `GET /api/payments/booking/:id` - Get payment by booking

### Reviews
- `POST /api/reviews` - Submit review
- `GET /api/reviews/host/:id` - Get host reviews

## 📁 File Structure

```
dbms/
├── server/
│   ├── server.js          # Backend API server
│   ├── .env               # Database credentials
│   ├── .env.example       # Template for .env
│   └── uploads/           # Image storage (auto-created)
├── src/
│   ├── services/
│   │   └── api.js         # API service layer
│   └── context/
│       └── AuthContext.jsx # Updated with API integration
├── create_tables.sql       # Updated schema with Image_URL
├── setup_database.py       # Updated setup script
└── add_image_column.sql    # Migration for existing DBs
```

## 🧪 Testing the Connection

1. **Test Backend Connection**
   ```bash
   curl http://localhost:5000/api/equipment/farm
   ```

2. **Test Signup**
   - Navigate to http://localhost:5173/signup
   - Fill out the form
   - Check MySQL database for new record

3. **Test Login**
   - Navigate to http://localhost:5173/login
   - Login with created account
   - Verify redirect to dashboard
