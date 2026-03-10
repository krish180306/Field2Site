import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dh10062006@10",
    database="rental_system"
)

cursor = conn.cursor()

try:
    print("Adding Equipment_Type column to tables...")
    
    # Add Equipment_Type column to FARM_EQUIPMENT
    cursor.execute("""
        ALTER TABLE FARM_EQUIPMENT 
        ADD COLUMN Equipment_Type VARCHAR(50) AFTER Equipment_Name
    """)
    print("✓ Added Equipment_Type to FARM_EQUIPMENT")
    
    # Add Equipment_Type column to CONSTRUCTION_EQUIPMENT
    cursor.execute("""
        ALTER TABLE CONSTRUCTION_EQUIPMENT 
        ADD COLUMN Equipment_Type VARCHAR(50) AFTER Equipment_Name
    """)
    print("✓ Added Equipment_Type to CONSTRUCTION_EQUIPMENT")
    
    conn.commit()
    print("\n" + "="*60)
    print("✅ Successfully added Equipment_Type columns!")
    print("="*60)
    
    # Now update existing data with appropriate types
    print("\nUpdating existing equipment with types...")
    
    # Farm Equipment updates
    farm_updates = [
        ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Tractor' WHERE Equipment_Name LIKE '%Tractor%'", "Tractors"),
        ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Harvester' WHERE Equipment_Name LIKE '%Harvest%' OR Equipment_Name LIKE '%Combine%'", "Harvesters"),
        ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Plow' WHERE Equipment_Name LIKE '%Rotavator%' OR Equipment_Name LIKE '%Plow%' OR Equipment_Name LIKE '%Till%'", "Plows"),
        ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Seeder' WHERE Equipment_Name LIKE '%Seed%' OR Equipment_Name LIKE '%Plant%'", "Seeders"),
        ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Sprayer' WHERE Equipment_Name LIKE '%Spray%' OR Equipment_Name LIKE '%Sprinkler%'", "Sprayers"),
        ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Other' WHERE Equipment_Type IS NULL", "Other farm equipment"),
    ]
    
    for query, desc in farm_updates:
        cursor.execute(query)
        if cursor.rowcount > 0:
            print(f"  ✓ Updated {cursor.rowcount} {desc}")
    
    # Construction Equipment updates
    construction_updates = [
        ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Excavator' WHERE Equipment_Name LIKE '%Excavat%' OR Equipment_Name LIKE '%JCB%'", "Excavators"),
        ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Bulldozer' WHERE Equipment_Name LIKE '%Bulldozer%' OR Equipment_Name LIKE '%Dozer%'", "Bulldozers"),
        ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Crane' WHERE Equipment_Name LIKE '%Crane%'", "Cranes"),
        ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Loader' WHERE Equipment_Name LIKE '%Loader%'", "Loaders"),
        ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Compactor' WHERE Equipment_Name LIKE '%Roller%' OR Equipment_Name LIKE '%Compact%'", "Compactors"),
        ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Other' WHERE Equipment_Type IS NULL", "Other construction equipment"),
    ]
    
    for query, desc in construction_updates:
        cursor.execute(query)
        if cursor.rowcount > 0:
            print(f"  ✓ Updated {cursor.rowcount} {desc}")
    
    conn.commit()
    
    print("\n" + "="*60)
    print("✅ Successfully updated all equipment types!")
    print("="*60)
    
    # Show summary
    print("\nSummary:")
    cursor.execute("SELECT Equipment_Type, COUNT(*) FROM FARM_EQUIPMENT GROUP BY Equipment_Type")
    print("\nFarm Equipment by Type:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    cursor.execute("SELECT Equipment_Type, COUNT(*) FROM CONSTRUCTION_EQUIPMENT GROUP BY Equipment_Type")
    print("\nConstruction Equipment by Type:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")

except mysql.connector.Error as err:
    if err.errno == 1060:  # Duplicate column name
        print("⚠️  Equipment_Type column already exists!")
        print("Skipping column creation, updating data only...")
        
        # Still try to update the data
        try:
            # Farm Equipment updates
            farm_updates = [
                ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Tractor' WHERE Equipment_Name LIKE '%Tractor%'", "Tractors"),
                ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Harvester' WHERE Equipment_Name LIKE '%Harvest%' OR Equipment_Name LIKE '%Combine%'", "Harvesters"),
                ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Plow' WHERE Equipment_Name LIKE '%Rotavator%' OR Equipment_Name LIKE '%Plow%' OR Equipment_Name LIKE '%Till%'", "Plows"),
                ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Seeder' WHERE Equipment_Name LIKE '%Seed%' OR Equipment_Name LIKE '%Plant%'", "Seeders"),
                ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Sprayer' WHERE Equipment_Name LIKE '%Spray%' OR Equipment_Name LIKE '%Sprinkler%'", "Sprayers"),
                ("UPDATE FARM_EQUIPMENT SET Equipment_Type = 'Other' WHERE Equipment_Type IS NULL", "Other farm equipment"),
            ]
            
            for query, desc in farm_updates:
                cursor.execute(query)
                if cursor.rowcount > 0:
                    print(f"  ✓ Updated {cursor.rowcount} {desc}")
            
            # Construction Equipment updates
            construction_updates = [
                ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Excavator' WHERE Equipment_Name LIKE '%Excavat%' OR Equipment_Name LIKE '%JCB%'", "Excavators"),
                ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Bulldozer' WHERE Equipment_Name LIKE '%Bulldozer%' OR Equipment_Name LIKE '%Dozer%'", "Bulldozers"),
                ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Crane' WHERE Equipment_Name LIKE '%Crane%'", "Cranes"),
                ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Loader' WHERE Equipment_Name LIKE '%Loader%'", "Loaders"),
                ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Compactor' WHERE Equipment_Name LIKE '%Roller%' OR Equipment_Name LIKE '%Compact%'", "Compactors"),
                ("UPDATE CONSTRUCTION_EQUIPMENT SET Equipment_Type = 'Other' WHERE Equipment_Type IS NULL", "Other construction equipment"),
            ]
            
            for query, desc in construction_updates:
                cursor.execute(query)
                if cursor.rowcount > 0:
                    print(f"  ✓ Updated {cursor.rowcount} {desc}")
            
            conn.commit()
            print("\n✅ Data updated successfully!")
        except Exception as e:
            print(f"❌ Error updating data: {e}")
            conn.rollback()
    else:
        print(f"❌ Error: {err}")
        conn.rollback()

finally:
    cursor.close()
    conn.close()
