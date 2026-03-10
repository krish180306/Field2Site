-- Migration script to add Image_URL column to existing equipment tables
-- Run this if you already have the database created

USE rental_system;

-- Add Image_URL column to FARM_EQUIPMENT table
ALTER TABLE FARM_EQUIPMENT 
ADD COLUMN Image_URL VARCHAR(500) AFTER Year_Of_Manufacture;

-- Add Image_URL column to CONSTRUCTION_EQUIPMENT table
ALTER TABLE CONSTRUCTION_EQUIPMENT 
ADD COLUMN Image_URL VARCHAR(500) AFTER Year_Of_Manufacture;

-- Verify the changes
DESCRIBE FARM_EQUIPMENT;
DESCRIBE CONSTRUCTION_EQUIPMENT;
