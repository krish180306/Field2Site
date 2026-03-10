import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="rental_system"
)

cursor = conn.cursor()

try:
    # Check existing hosts
    cursor.execute("SELECT Host_ID, Host_Name FROM HOST")
    hosts = cursor.fetchall()
    print("Existing hosts:")
    for h in hosts:
        print(f"  ID {h[0]}: {h[1]}")
    
    print("\nAttempting to insert construction equipment with Host_ID=2...")
    cursor.execute("""
    INSERT INTO CONSTRUCTION_EQUIPMENT (Host_ID, Equipment_Name, Power_Source, Capacity, Hourly_Rate, Daily_Rate, Availability_Status)
    VALUES (2, 'JCB Excavator', 'Diesel', '1.2 m3 Bucket', 1200, 8500, 'Available')
    """)
    conn.commit()
    print("✅ Success!")
    
    # Check what was inserted
    cursor.execute("SELECT * FROM CONSTRUCTION_EQUIPMENT")
    equipment = cursor.fetchall()
    print(f"\nTotal construction equipment: {len(equipment)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    cursor.close()
    conn.close()
