-- Migration: Add Password column to HOST and BUYER tables
-- Run: mysql -u root -p rental_system < add_password_column.sql

ALTER TABLE HOST ADD COLUMN Password VARCHAR(255) NOT NULL DEFAULT 'field2site123';
ALTER TABLE BUYER ADD COLUMN Password VARCHAR(255) NOT NULL DEFAULT 'field2site123';

-- Set default password for all existing users
UPDATE HOST SET Password = 'field2site123';
UPDATE BUYER SET Password = 'field2site123';

SELECT 'Migration complete. All existing users password: field2site123' AS Status;
