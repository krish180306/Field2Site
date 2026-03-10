import mysql.connector

# ---------- DB CONNECTION ----------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dh10062006@10",
    database="rental_system"
)

cursor = conn.cursor()

# Clear existing data (in reverse order of dependencies)
print("Clearing existing data...")
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("TRUNCATE TABLE REVIEW")
cursor.execute("TRUNCATE TABLE MAINTENANCE")
cursor.execute("TRUNCATE TABLE PAYMENT")
cursor.execute("TRUNCATE TABLE BOOKING")
cursor.execute("TRUNCATE TABLE CONSTRUCTION_EQUIPMENT")
cursor.execute("TRUNCATE TABLE FARM_EQUIPMENT")
cursor.execute("TRUNCATE TABLE BUYER")
cursor.execute("TRUNCATE TABLE HOST")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
conn.commit()
print("✓ Existing data cleared\n")

# ---------- INSERT HOST ----------
print("Inserting hosts...")
hosts = [
    ('Ramesh Kumar', 'Individual', '9876543210', 'ramesh@farmrent.com', '12 Green Street', 'Coimbatore', 'Tamil Nadu', '641001', 4.5, 1),
    ('Arun Builders', 'Company', '9123456780', 'arun@buildrent.com', '45 Industrial Road', 'Chennai', 'Tamil Nadu', '600001', 4.2, 1),
    ('Suresh Agro Equip', 'Individual', '9988776655', 'suresh@agroequip.com', '88 Farm Lane', 'Madurai', 'Tamil Nadu', '625001', 4.0, 1),
    ('Karthik Rentals', 'Company', '9090909090', 'karthik@rentals.com', '10 Main Bazaar', 'Bangalore', 'Karnataka', '560001', 3.9, 0),
    ('Vijay Machinery Hub', 'Dealer', '9555443322', 'vijay@machhub.com', '23 Market Street', 'Trichy', 'Tamil Nadu', '620001', 4.7, 1)
]

cursor.executemany("""
INSERT INTO HOST (Host_Name, Host_Type, Phone, Email, Address, City, State, Pincode, Rating, Verified_Status)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""", hosts)
conn.commit()
print(f"✓ Inserted {len(hosts)} hosts")


# ---------- INSERT BUYER ----------
print("Inserting buyers...")
buyers = [
    ('Farm', 'Manoj Farmer', '9877001122', 'manoj@gmail.com', 'Village Road 3', 'Salem', 'Tamil Nadu', '636001'),
    ('Construction', 'Deepak Constructions', '9098776655', 'deepak@construct.com', 'Site Area 5', 'Chennai', 'Tamil Nadu', '600002'),
    ('Farm', 'Lakshmi Agro', '9888112233', 'lakshmi@agro.com', 'Agro Market 9', 'Erode', 'Tamil Nadu', '638001'),
    ('Construction', 'Naveen Civil Works', '9011223344', 'naveen@civil.com', 'Ring Road', 'Bangalore', 'Karnataka', '560002'),
    ('Farm', 'Prakash Fields', '9898989898', 'prakash@fields.com', 'Farm House 12', 'Tanjore', 'Tamil Nadu', '613001')
]

cursor.executemany("""
INSERT INTO BUYER (Buyer_Type, Name, Phone, Email, Address, City, State, Pincode)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
""", buyers)
conn.commit()
print(f"✓ Inserted {len(buyers)} buyers")


# ---------- INSERT FARM_EQUIPMENT ----------
print("Inserting farm equipment...")
farm_equipment = [
    (1, 'John Deere Tractor', 'Diesel', '50 HP', 500, 3500, 'Available'),
    (3, 'Rotavator', 'Tractor Attachment', '6 Feet', 200, 1200, 'Available'),
    (5, 'Seeder Machine', 'Diesel', '8 Rows', 250, 1500, 'Rented'),
    (1, 'Water Pump Set', 'Electric', '5 HP', 100, 600, 'Available'),
    (5, 'Harvesting Combine', 'Diesel', '2 Acre/hr', 800, 6000, 'Maintenance')
]

cursor.executemany("""
INSERT INTO FARM_EQUIPMENT (Host_ID, Equipment_Name, Power_Source, Capacity, Hourly_Rate, Daily_Rate, Availability_Status)
VALUES (%s,%s,%s,%s,%s,%s,%s)
""", farm_equipment)
conn.commit()
print(f"✓ Inserted {len(farm_equipment)} farm equipment")


# ---------- INSERT CONSTRUCTION_EQUIPMENT ----------
print("Inserting construction equipment...")
construction_equipment = [
    (2, 'JCB Excavator', 'Diesel', '1.2 m3 Bucket', 1200, 8500, 'Available'),
    (4, 'Concrete Mixer', 'Electric', '500 Litres', 400, 2500, 'Available'),
    (2, 'Hydraulic Crane', 'Diesel', '10 Tons', 1500, 11000, 'Rented'),
    (4, 'Road Roller', 'Diesel', '8 Tons', 1000, 7500, 'Available'),
    (2, 'Drilling Machine', 'Electric', 'Heavy Duty', 600, 4000, 'Maintenance')
]

cursor.executemany("""
INSERT INTO CONSTRUCTION_EQUIPMENT (Host_ID, Equipment_Name, Power_Source, Capacity, Hourly_Rate, Daily_Rate, Availability_Status)
VALUES (%s,%s,%s,%s,%s,%s,%s)
""", construction_equipment)
conn.commit()
print(f"✓ Inserted {len(construction_equipment)} construction equipment\n")


# ---------- SHOW SUMMARY ----------
print("=" * 60)
print("✅ All data inserted successfully!")
print("=" * 60)

# Show summary
cursor.execute("SELECT COUNT(*) FROM HOST")
print(f"📊 Total Hosts: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM BUYER")
print(f"📊 Total Buyers: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM FARM_EQUIPMENT")
print(f"📊 Total Farm Equipment: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM CONSTRUCTION_EQUIPMENT")
print(f"📊 Total Construction Equipment: {cursor.fetchone()[0]}")

print("=" * 60)
print("\n💡 Note: BOOKING, PAYMENT, REVIEW, and MAINTENANCE tables")
print("   were skipped due to complex foreign key dependencies.")
print("   You can add them through the application interface.")
print("=" * 60)

cursor.close()
conn.close()