-- Database: ict_inventory_db

-- DROP DATABASE IF EXISTS ict_inventory_db;

CREATE DATABASE ict_inventory_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE ict_inventory_db
    IS 'Main database for ICT Asset Inventory System';