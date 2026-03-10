"""
Tractor & Equipment Rental System - Database Setup Script
This script creates the database schema from the SQL file.
"""

import mysql.connector
from mysql.connector import Error

class DatabaseSetup:
    def __init__(self, host='localhost', user='root', password='', database='rental_system'):
        """Initialize database connection parameters"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self):
        """Create database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print(f"✓ Connected to MySQL Server")
                return True
        except Error as e:
            print(f"✗ Error connecting to MySQL: {e}")
            return False
    
    def create_database(self):
        """Create the database if it doesn't exist"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.database}")
            cursor.execute(f"CREATE DATABASE {self.database}")
            cursor.execute(f"USE {self.database}")
            print(f"✓ Database '{self.database}' created and selected")
            cursor.close()
            return True
        except Error as e:
            print(f"✗ Error creating database: {e}")
            return False
    
    def create_tables(self):
        """Create all tables directly"""
        try:
            cursor = self.connection.cursor()
            
            # Create HOST table
            cursor.execute("""
                CREATE TABLE HOST (
                    Host_ID INT PRIMARY KEY AUTO_INCREMENT,
                    Host_Name VARCHAR(100) NOT NULL,
                    Host_Type VARCHAR(50),
                    Phone VARCHAR(15),
                    Email VARCHAR(100) UNIQUE,
                    Address VARCHAR(255),
                    City VARCHAR(100),
                    State VARCHAR(100),
                    Pincode VARCHAR(10),
                    Rating DECIMAL(3,2) DEFAULT 0.00,
                    Verified_Status BOOLEAN DEFAULT FALSE,
                    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("✓ Created HOST table")
            
            # Create BUYER table
            cursor.execute("""
                CREATE TABLE BUYER (
                    Buyer_ID INT PRIMARY KEY AUTO_INCREMENT,
                    Buyer_Type ENUM('Farm', 'Construction') NOT NULL,
                    Name VARCHAR(100) NOT NULL,
                    Phone VARCHAR(15),
                    Email VARCHAR(100) UNIQUE,
                    Address VARCHAR(255),
                    City VARCHAR(100),
                    State VARCHAR(100),
                    Pincode VARCHAR(10),
                    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("✓ Created BUYER table")
            
            # Create FARM_EQUIPMENT table
            cursor.execute("""
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
                )
            """)
            print("✓ Created FARM_EQUIPMENT table")
            
            # Create CONSTRUCTION_EQUIPMENT table
            cursor.execute("""
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
                )
            """)
            print("✓ Created CONSTRUCTION_EQUIPMENT table")
            
            # Create BOOKING table
            cursor.execute("""
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
                )
            """)
            print("✓ Created BOOKING table")
            
            # Create PAYMENT table
            cursor.execute("""
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
                )
            """)
            print("✓ Created PAYMENT table")
            
            # Create MAINTENANCE table
            cursor.execute("""
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
                )
            """)
            print("✓ Created MAINTENANCE table")
            
            # Create REVIEW table
            cursor.execute("""
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
                )
            """)
            print("✓ Created REVIEW table")
            
            # Create indexes
            print("\nCreating indexes...")
            cursor.execute("CREATE INDEX idx_farm_equipment_host ON FARM_EQUIPMENT(Host_ID)")
            cursor.execute("CREATE INDEX idx_farm_equipment_status ON FARM_EQUIPMENT(Availability_Status)")
            cursor.execute("CREATE INDEX idx_construction_equipment_host ON CONSTRUCTION_EQUIPMENT(Host_ID)")
            cursor.execute("CREATE INDEX idx_construction_equipment_status ON CONSTRUCTION_EQUIPMENT(Availability_Status)")
            cursor.execute("CREATE INDEX idx_booking_buyer ON BOOKING(Buyer_ID)")
            cursor.execute("CREATE INDEX idx_booking_host ON BOOKING(Host_ID)")
            cursor.execute("CREATE INDEX idx_booking_status ON BOOKING(Status)")
            cursor.execute("CREATE INDEX idx_booking_dates ON BOOKING(Start_Date, End_Date)")
            cursor.execute("CREATE INDEX idx_payment_booking ON PAYMENT(Booking_ID)")
            cursor.execute("CREATE INDEX idx_payment_status ON PAYMENT(Status)")
            cursor.execute("CREATE INDEX idx_review_host ON REVIEW(Host_ID)")
            cursor.execute("CREATE INDEX idx_maintenance_equipment ON MAINTENANCE(Equipment_ID, Equipment_DB)")
            print("✓ Created all indexes")
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            print(f"✗ Error creating tables: {e}")
            return False
    
    def display_summary(self):
        """Display summary of created tables"""
        try:
            cursor = self.connection.cursor()
            
            tables = ['HOST', 'BUYER', 'FARM_EQUIPMENT', 'CONSTRUCTION_EQUIPMENT', 
                     'BOOKING', 'PAYMENT', 'MAINTENANCE', 'REVIEW']
            
            print("\n" + "="*60)
            print("DATABASE SUMMARY")
            print("="*60)
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table:30} : {count:5} records")
            
            print("="*60)
            cursor.close()
            
        except Error as e:
            print(f"✗ Error displaying summary: {e}")
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("\n✓ Database connection closed")


def main():
    """Main execution function"""
    print("="*60)
    print("TRACTOR & EQUIPMENT RENTAL SYSTEM - DATABASE SETUP")
    print("="*60)
    print()
    
    # Get database credentials
    print("Enter MySQL credentials:")
    host = input("Host (default: localhost): ").strip() or 'localhost'
    user = input("Username (default: root): ").strip() or 'root'
    password = input("Password: ").strip()
    database = input("Database name (default: rental_system): ").strip() or 'rental_system'
    
    print()
    
    # Initialize setup
    db_setup = DatabaseSetup(host=host, user=user, password=password, database=database)
    
    # Connect to MySQL
    if not db_setup.connect():
        return
    
    # Create database
    if not db_setup.create_database():
        db_setup.close()
        return
    
    # Create tables
    if not db_setup.create_tables():
        db_setup.close()
        return
    
    # Display summary
    db_setup.display_summary()
    
    # Close connection
    db_setup.close()
    
    print("\n✓ Setup completed successfully!")
    print(f"\nYou can now connect to the '{database}' database and start using it!")


if __name__ == "__main__":
    main()
