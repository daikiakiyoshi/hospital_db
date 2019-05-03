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
    print(header)

    values = [f"\'{str(params[prop])}\'" for prop in header]

    sql = f"""INSERT INTO {select}({", ".join(header)}) VALUES ({", ".join(values)});"""
    print(sql)

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

    print(sql)

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

def delete(select, id):
    header = get_header(select)

    sql = f"""
        DELETE FROM {select}
        WHERE {header[0]} = {id};
    """

    print(sql)

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
