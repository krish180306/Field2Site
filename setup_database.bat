@echo off
REM Tractor & Equipment Rental System - Database Setup Script
REM This batch script creates the database and tables using MySQL command line

echo ============================================================
echo TRACTOR ^& EQUIPMENT RENTAL SYSTEM - DATABASE SETUP
echo ============================================================
echo.

REM Get MySQL credentials
set /p MYSQL_USER="Enter MySQL username (default: root): "
if "%MYSQL_USER%"=="" set MYSQL_USER=root

set /p MYSQL_PASSWORD="Enter MySQL password: "

set /p DATABASE_NAME="Enter database name (default: rental_system): "
if "%DATABASE_NAME%"=="" set DATABASE_NAME=rental_system

echo.
echo Connecting to MySQL and creating database...
echo.

REM Create database
mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS %DATABASE_NAME%;"

if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to create database. Please check your credentials.
    pause
    exit /b 1
)

echo Database '%DATABASE_NAME%' created/selected
echo.
echo Executing SQL schema...
echo.

REM Execute SQL file
mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% %DATABASE_NAME% < create_tables.sql

if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to execute SQL schema.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS! All tables have been created.
echo ============================================================
echo.
echo Database: %DATABASE_NAME%
echo Tables created:
echo   - HOST
echo   - BUYER
echo   - FARM_EQUIPMENT
echo   - CONSTRUCTION_EQUIPMENT
echo   - BOOKING
echo   - PAYMENT
echo   - MAINTENANCE
echo   - REVIEW
echo.
echo You can now connect to your database and start adding data.
echo.
pause
