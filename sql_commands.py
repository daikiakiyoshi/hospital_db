CREATE_DOCTORS = """
    CREATE TABLE doctors (
        doc_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        title VARCHAR(255) NOT NULL
    )
"""

CREATE_DEPARTMENTS = """
    CREATE TABLE departments (
        dep_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
"""

# TODO: check if this is the correct way to specify the types of the attributes
CREATE_DEPARTMENTS = """
    CREATE TABLE WorksFor (
        dep_id INTEGER PRIMARY KEY,
        dep_id INTEGER PRIMARY KEY
    )
"""

CREATE_PATIENT_RECORDS = """
    CREATE TABLE patient_records (
        p_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INTEGER,
        ssn VARCHAR(255),
        date_in DATE,
        date_out DATE,
        diagnosis VARCHAR(255)
    )
"""

CREATE_TREATED_BY = """
    CREATE TABLE patient_records (
        doc_id INTEGER PRIMARY KEY,
        p_id INTEGER PRIMARY KEY
    )
"""

CREATE_SERVICE = """
    CREATE TABLE patient_records (
        serv_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2),
        unit_type VARCHAR(255) NOT NULL
    )
"""

CREATE_MEDICINE = """
    CREATE TABLE patient_records (
        med_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2),
        unit_type VARCHAR(255) NOT NULL
    )
"""

CREATE_BILLED_SERVICE = """
    CREATE TABLE billed_service (
        p_id INTEGER PRIMARY KEY,
        serv_id INTEGER PRIMARY KEY,
        units INTEGER,
        status VARCHAR(255) NOT NULL
    )
"""

CREATE_BILLED_MEDICINE = """
    CREATE TABLE billed_medicine (
        p_id INTEGER PRIMARY KEY,
        med_id INTEGER PRIMARY KEY,
        units INTEGER,
        status VARCHAR(255) NOT NULL
    )
"""

CREATE_ROOMS = """
    CREATE TABLE rooms (
        room_id VARCHAR(255) PRIMARY KEY,
        room_type VARCHAR(255),
        max_beds INTEGER,
        available_beds INTEGER,
    )
"""

STAYS_IN = """
    CREATE TABLE stays_in (
        p_id INTEGER PRIMARY KEY,
        room_id VARCHAR(255) PRIMARY KEY
    )
"""
