import sqlite3
import re
import os

def create_db(schema_file,file_dir = 'folder/',db_filename='dhcp_snooping.db'):
    schema_filename = file_dir + schema_file
    db_exists = os.path.exists(db_filename)
    if not db_exists:
        print('Creating schema...')
        conn = sqlite3.connect(db_filename)
        with open(schema_filename) as f:
            schema = f.read()
        conn.executescript(schema)
        conn.close()
        print ('"dhcp_snooping.db" DATABASE CREATED SUCCESSFULLY')
        return
    else:
        print('Database exists, assume dhcp table does, too.')
        return
if __name__ == "__main__":
    new_db = 'dhcp_snooping_schema.sql'
    create_db(new_db)


