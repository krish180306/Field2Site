import mysql.connector
import json

# Connect to database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='rental_system'
)

cursor = conn.cursor(dictionary=True)

print("=" * 80)
print("DATABASE VERIFICATION - Signup Integration Test")
print("=" * 80)
print()

# Check BUYER table
print("📊 BUYER TABLE:")
print("-" * 80)
cursor.execute("SELECT Buyer_ID, Name, Email, Phone, Buyer_Type, City, State, Created_At FROM BUYER")
buyers = cursor.fetchall()
if buyers:
    for buyer in buyers:
        print(f"  ID: {buyer['Buyer_ID']}")
        print(f"  Name: {buyer['Name']}")
        print(f"  Email: {buyer['Email']}")
        print(f"  Phone: {buyer['Phone']}")
        print(f"  Type: {buyer['Buyer_Type']}")
        print(f"  Location: {buyer['City']}, {buyer['State']}")
        print(f"  Created: {buyer['Created_At']}")
        print("-" * 80)
else:
    print("  No buyers found")
    print("-" * 80)

print()

# Check HOST table
print("🏢 HOST TABLE:")
print("-" * 80)
cursor.execute("SELECT Host_ID, Host_Name, Email, Phone, Host_Type, City, State, Created_At FROM HOST")
hosts = cursor.fetchall()
if hosts:
    for host in hosts:
        print(f"  ID: {host['Host_ID']}")
        print(f"  Name: {host['Host_Name']}")
        print(f"  Email: {host['Email']}")
        print(f"  Phone: {host['Phone']}")
        print(f"  Type: {host['Host_Type']}")
        print(f"  Location: {host['City']}, {host['State']}")
        print(f"  Created: {host['Created_At']}")
        print("-" * 80)
else:
    print("  No hosts found")
    print("-" * 80)

print()
print("=" * 80)
print(f"✅ Total Buyers: {len(buyers)}")
print(f"✅ Total Hosts: {len(hosts)}")
print("=" * 80)

cursor.close()
conn.close()
