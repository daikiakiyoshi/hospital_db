import psycopg2
from config import config
import sql_commands 

def create_tables():
    commands = tuple(sql_commands.CREATE_STATEMENTS)
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


def insert(params, select, table_with_id):
    header = get_header(select)

    if select not in table_with_id:
        header = header[1:]

    values = [f"\'{str(params[prop])}\'" for prop in header]

    sql = f"""INSERT INTO {select}({", ".join(header)}) VALUES ({", ".join(values)});"""

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_query(select):
    conn = None
    header = get_header(select)
    data = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {select}")
        row = cur.fetchone()
        while row is not None:
            toAdd = {}
            for i in range(len(header)):
                toAdd[header[i]] = row[i]
            data.append(toAdd)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return data

def filter(select, values):
    conn = None
    header = get_header(select)
    values = [f"\'{str(values[prop])}\'" for prop in values.keys()]

    values = [prop + "=" + f"\'{str(values[prop])}\'" for prop in values.keys()]
    values = ", ".join(values)
    print(values)
    data = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {select} WHERE {values}")
        row = cur.fetchone()
        while row is not None:
            toAdd = {}
            for i in range(len(header)):
                toAdd[header[i]] = row[i]
            data.append(toAdd)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return data

def update(select, id, params):
    header = get_header(select)

    values = [f"\'{str(params[prop])}\'" for prop in params.keys()]

    values = [prop + "=" + f"\'{str(params[prop])}\'" for prop in params.keys()]
    values = ", ".join(values)
    print(values)

    sql = f"""
        UPDATE {select}
        SET {values}
        WHERE {header[0]} = {id};
    """

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_header(select):
    """ query data from the vendors table """
    conn = None
    header = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {select} LIMIT 0")
        header = [desc[0] for desc in cur.description]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return header

if __name__ == '__main__':
    create_tables()


def get_total_bill(p_id):
    """Get the total bill for a patient record given the patient record id"""
    get_all_services = f"""
        SELECT *
        FROM billed_service
        WHERE p_id = {p_id}
    """

    get_all_meds = f"""
        SELECT *
        FROM billed_medicine
        WHERE p_id = {p_id}
    """
    
    total_bill = 0

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # find billed medicines and services and add the the bill
        cur.execute(get_all_services)
        all_billed_services = cur.fetchall()
        for serv in all_billed_services:
            id, units = serv[1], serv[2]
            
            cur.execute(f"""
                SELECT price
                FROM service
                WHERE serv_id = {id}
            """)

            total_bill += units * cur.fetchone()[0]

        cur.execute(get_all_meds)
        all_billed_meds = cur.fetchall()
        for med in all_billed_meds:
            id, units = med[1], med[2]
            
            cur.execute(f"""
                SELECT price
                FROM medicine
                WHERE med_id = {id}
            """)

            total_bill += units * cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return total_bill
    
print(get_total_bill(1))