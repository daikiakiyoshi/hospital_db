import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE patients (
            p_id SERIAL PRIMARY KEY,
            fname VARCHAR(255) NOT NULL,
            lname VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE doctors (
                doc_id SERIAL PRIMARY KEY,
                fname VARCHAR(255) NOT NULL,
                lname VARCHAR(255) NOT NULL
                )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_patient(fname, lname):
    """ insert a new patient into the patients table """
    sql = """INSERT INTO patients(fname, lname)
             VALUES(%s, %s);"""
    conn = None
    patient_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (fname, lname))
        #cur.execute("INSERT INTO Patients(fname, lname) VALUES('Daiki','Akiyoshi')")
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_patients():
    """ query data from the vendors table """
    conn = None
    data = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients")
        row = cur.fetchone()
        while row is not None:
            data.append(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return data

if __name__ == '__main__':
    create_tables()