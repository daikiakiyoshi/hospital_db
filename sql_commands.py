DROP_ALL = """
    drop table if exists doctors CASCADE;
    drop table if exists departments CASCADE;
    drop table if exists worksfor CASCADE;
    drop table if exists patient_records CASCADE;
    drop table if exists treatedby CASCADE;
    drop table if exists service CASCADE;
    drop table if exists medicine CASCADE;
    drop table if exists billed_service CASCADE;
    drop table if exists billed_medicine CASCADE;
    drop table if exists rooms CASCADE;
    drop table if exists stays_in CASCADE;
"""

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
CREATE_WORKSFOR = """
    CREATE TABLE worksfor (
        doc_id INTEGER REFERENCES doctors(doc_id),
        dep_id INTEGER REFERENCES departments(dep_id)
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
    CREATE TABLE treatedby (
        doc_id INTEGER REFERENCES doctors(doc_id),
        p_id INTEGER REFERENCES patient_records(p_id)
    )
"""

CREATE_SERVICE = """
    CREATE TABLE service (
        serv_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2),
        unit_type VARCHAR(255) NOT NULL
    )
"""

CREATE_MEDICINE = """
    CREATE TABLE medicine (
        med_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2),
        unit_type VARCHAR(255) NOT NULL
    )
"""

CREATE_BILLED_SERVICE = """
    CREATE TABLE billed_service (
        p_id INTEGER REFERENCES patient_records(p_id),
        serv_id INTEGER REFERENCES service(serv_id),
        units INTEGER,
        status VARCHAR(255) NOT NULL
    )
"""

CREATE_BILLED_MEDICINE = """
    CREATE TABLE billed_medicine (
        p_id INTEGER REFERENCES patient_records(p_id),
        med_id INTEGER REFERENCES medicine(med_id),
        units INTEGER,
        status VARCHAR(255) NOT NULL
    )
"""

CREATE_ROOMS = """
    CREATE TABLE rooms (
        room_id VARCHAR(255) PRIMARY KEY,
        room_type VARCHAR(255),
        max_beds INTEGER,
        available_beds INTEGER
    )
"""

STAYS_IN = """
    CREATE TABLE stays_in (
        p_id INTEGER REFERENCES patient_records(p_id),
        room_id VARCHAR(255) REFERENCES rooms(room_id)
    )
"""

INSERT_PATIENTS = """
    INSERT INTO patient_records(name, age, ssn, date_in, date_out, diagnosis)
    VALUES
        ('james', '20', '123145', '2017-03-14', '2017-03-14', 'healthy'),
        ('daiki', '20', '123145', '2017-03-14', '2017-03-14', 'healthy');
"""

INSERT_DOCTORS = """
    INSERT INTO doctors(name, title)
    VALUES
        ('Doctor 1', 'Title 1'),
        ('Doctor 2', 'Title 2'),
        ('Doctor 3', 'Title 3'),
        ('Doctor 4', 'Title 4'),
        ('Doctor 5', 'Title 5');
"""

INSERT_DEPARTMENTS = """
    INSERT INTO departments(name)
    VALUES
        ('Dep 1'),
        ('Dep 2'),
        ('Dep 3'),
        ('Dep 4'),
        ('Dep 5');
"""

INSERT_SERVICES = """
    INSERT INTO service(name, category, price, unit_type)
    VALUES
        ('serv 1', 'cat', 2.00, 'day'),
        ('serv 2', 'cat', 2.00, 'day'),
        ('serv 3', 'cat', 2.00, 'day'),
        ('serv 4', 'cat', 2.00, 'day'),
        ('serv 5', 'cat', 2.00, 'day');
"""

INSERT_MEDICINE = """
    INSERT INTO medicine(name, price, unit_type)
    VALUES
        ('med 1', 1.00, 'tablet'),
        ('med 2', 1.00, 'tablet'),
        ('med 3', 1.00, 'tablet'),
        ('med 4', 1.00, 'tablet'),
        ('med 5', 1.00, 'tablet');
"""

INSERT_BILLED_MED = """
    INSERT INTO billed_medicine (p_id, med_id, units, status)
    VALUES
        (1, 1, 20, 'Unpaid'),
        (1, 2, 10, 'Unpaid')
"""

INSERT_BILLED_SERV = """
    INSERT INTO billed_service (p_id, serv_id, units, status)
    VALUES
        (1, 1, 2, 'Unpaid'),
        (1, 2, 1, 'Unpaid')
"""

CREATE_STATEMENTS = [DROP_ALL, CREATE_DOCTORS, CREATE_DEPARTMENTS, CREATE_WORKSFOR, CREATE_PATIENT_RECORDS,
                        CREATE_TREATED_BY, CREATE_SERVICE, CREATE_MEDICINE, CREATE_BILLED_SERVICE,
                        CREATE_BILLED_MEDICINE, CREATE_ROOMS, STAYS_IN, INSERT_DOCTORS, INSERT_DEPARTMENTS, INSERT_PATIENTS,
                        INSERT_MEDICINE, INSERT_SERVICES,
                        INSERT_BILLED_MED, INSERT_BILLED_SERV]
