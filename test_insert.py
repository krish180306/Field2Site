import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="rental_system"
)

cursor = conn.cursor()

try:
    cursor.execute("""
    INSERT INTO HOST (Host_Name, Host_Type, Phone, Email, Address, City, State, Pincode, Rating, Verified_Status)
    VALUES ('Test Host', 'Individual', '1234567890', 'testhost@test.com', '123 Test St', 'TestCity', 'TestState', '123456', 4.5, 1)
    """)
    conn.commit()
    print("✅ Insert successful!")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    cursor.close()
    conn.close()
