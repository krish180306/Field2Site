-- Tractor & Equipment Rental System Database Schema
-- Created: 2026-02-14

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS REVIEW;
DROP TABLE IF EXISTS MAINTENANCE;
DROP TABLE IF EXISTS PAYMENT;
DROP TABLE IF EXISTS BOOKING;
DROP TABLE IF EXISTS CONSTRUCTION_EQUIPMENT;
DROP TABLE IF EXISTS FARM_EQUIPMENT;
DROP TABLE IF EXISTS BUYER;
DROP TABLE IF EXISTS HOST;

-- Create HOST table
CREATE TABLE HOST (
    Host_ID INT PRIMARY KEY AUTO_INCREMENT,
    Host_Name VARCHAR(100) NOT NULL,
    Host_Type VARCHAR(50),
    Phone VARCHAR(15),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(255) NOT NULL DEFAULT 'field2site123',
    Address VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(100),
    Pincode VARCHAR(10),
    Rating DECIMAL(3,2) DEFAULT 0.00,
    Verified_Status BOOLEAN DEFAULT FALSE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create BUYER table
CREATE TABLE BUYER (
    Buyer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Buyer_Type ENUM('Farm', 'Construction') NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(15),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(255) NOT NULL DEFAULT 'field2site123',
    Address VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(100),
    Pincode VARCHAR(10),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create FARM_EQUIPMENT table
CREATE TABLE FARM_EQUIPMENT (
    Equipment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Host_ID INT NOT NULL,
    Equipment_Name VARCHAR(100) NOT NULL,
    Power_Source VARCHAR(50),
    Capacity VARCHAR(50),
    Hourly_Rate DECIMAL(10,2) NOT NULL,
    Daily_Rate DECIMAL(10,2) NOT NULL,
    Availability_Status ENUM('Available', 'Rented', 'Maintenance', 'Unavailable') DEFAULT 'Available',
    Description TEXT,
    Year_Of_Manufacture INT,
    Image_URL VARCHAR(500),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Host_ID) REFERENCES HOST(Host_ID) ON DELETE CASCADE
);

-- Create CONSTRUCTION_EQUIPMENT table
CREATE TABLE CONSTRUCTION_EQUIPMENT (
    Equipment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Host_ID INT NOT NULL,
    Equipment_Name VARCHAR(100) NOT NULL,
    Power_Source VARCHAR(50),
    Capacity VARCHAR(50),
    Hourly_Rate DECIMAL(10,2) NOT NULL,
    Daily_Rate DECIMAL(10,2) NOT NULL,
    Availability_Status ENUM('Available', 'Rented', 'Maintenance', 'Unavailable') DEFAULT 'Available',
    Description TEXT,
    Year_Of_Manufacture INT,
    Image_URL VARCHAR(500),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Host_ID) REFERENCES HOST(Host_ID) ON DELETE CASCADE
);

-- Create BOOKING table
CREATE TABLE BOOKING (
    Booking_ID INT PRIMARY KEY AUTO_INCREMENT,
    Buyer_ID INT NOT NULL,
    Host_ID INT NOT NULL,
    Equipment_ID INT NOT NULL,
    Equipment_Type ENUM('Farm', 'Construction') NOT NULL,
    Start_Date DATETIME NOT NULL,
    End_Date DATETIME NOT NULL,
    Usage_Type ENUM('Hourly', 'Daily') NOT NULL,
    Total_Amount DECIMAL(10,2) NOT NULL,
    Status ENUM('Pending', 'Confirmed', 'Completed', 'Cancelled') DEFAULT 'Pending',
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Buyer_ID) REFERENCES BUYER(Buyer_ID) ON DELETE CASCADE,
    FOREIGN KEY (Host_ID) REFERENCES HOST(Host_ID) ON DELETE CASCADE
);

-- Create PAYMENT table
CREATE TABLE PAYMENT (
    Payment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Booking_ID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Mode ENUM('Cash', 'Card', 'UPI', 'Net Banking', 'Wallet') NOT NULL,
    Status ENUM('Pending', 'Completed', 'Failed', 'Refunded') DEFAULT 'Pending',
    Payment_Date DATETIME,
    Transaction_ID VARCHAR(100) UNIQUE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Booking_ID) REFERENCES BOOKING(Booking_ID) ON DELETE CASCADE
);

-- Create MAINTENANCE table
CREATE TABLE MAINTENANCE (
    Maintenance_ID INT PRIMARY KEY AUTO_INCREMENT,
    Equipment_DB VARCHAR(50) NOT NULL COMMENT 'Database/Table name (FARM_EQUIPMENT or CONSTRUCTION_EQUIPMENT)',
    Equipment_Table_Name VARCHAR(100) NOT NULL,
    Equipment_ID INT NOT NULL,
    Service_Date DATE NOT NULL,
    Description TEXT,
    Cost DECIMAL(10,2),
    Next_Service_Date DATE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create REVIEW table
CREATE TABLE REVIEW (
    Review_ID INT PRIMARY KEY AUTO_INCREMENT,
    Booking_ID INT NOT NULL,
    Host_ID INT NOT NULL,
    Rating DECIMAL(3,2) NOT NULL CHECK (Rating >= 0 AND Rating <= 5),
    Comment TEXT,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Booking_ID) REFERENCES BOOKING(Booking_ID) ON DELETE CASCADE,
    FOREIGN KEY (Host_ID) REFERENCES HOST(Host_ID) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_farm_equipment_host ON FARM_EQUIPMENT(Host_ID);
CREATE INDEX idx_farm_equipment_status ON FARM_EQUIPMENT(Availability_Status);
CREATE INDEX idx_construction_equipment_host ON CONSTRUCTION_EQUIPMENT(Host_ID);
CREATE INDEX idx_construction_equipment_status ON CONSTRUCTION_EQUIPMENT(Availability_Status);
CREATE INDEX idx_booking_buyer ON BOOKING(Buyer_ID);
CREATE INDEX idx_booking_host ON BOOKING(Host_ID);
CREATE INDEX idx_booking_status ON BOOKING(Status);
CREATE INDEX idx_booking_dates ON BOOKING(Start_Date, End_Date);
CREATE INDEX idx_payment_booking ON PAYMENT(Booking_ID);
CREATE INDEX idx_payment_status ON PAYMENT(Status);
CREATE INDEX idx_review_host ON REVIEW(Host_ID);
CREATE INDEX idx_maintenance_equipment ON MAINTENANCE(Equipment_ID, Equipment_DB);
