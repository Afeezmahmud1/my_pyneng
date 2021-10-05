import sqlite3
import re
import os
import yaml
import sys
from pprint import pprint


#                                         CREATE THE DATABASE
#                          =================================================
def create_db(args):
#def create_db(schema_file,db_file='dhcp_snooping.db',file_dir = 'folder/'):
    schema_file = str(args.schema)
    schema_filename = 'folder/' + schema_file
    db_name = str(args.name)
    db_exists = os.path.exists(db_name)
    if not db_exists:
        print('Creating schema...')
        conn = sqlite3.connect(db_name)
        with open(schema_filename) as f:
            schema = f.read()
        conn.executescript(schema)
        conn.close()
        print ('"dhcp_snooping.db" DATABASE CREATED SUCCESSFULLY')
        return
    else:
        print('Database exists, assume dhcp table does, too.')
        return

#                                  ADD ENTRY TO TABLES IN THE DATABASE
#                              ===========================================
# internal function used to add files to the database
#------------------------------------------------------
def add_data_to_db (db_name,table_data,query):
    conn = sqlite3.connect(db_name)
    name = re.search('\w+ \w+ (\w+) \w+ \([?, ]+\)',query)
    #name = re.search('\w+ \w+ (\w+) \([a-z, ]+\) \w+ \([?, ]+\)',query)
    table_name = name.groups()[0]
    conn.execute("update dhcp set active = 0")
    print (f"Writing data into {table_name} table of database {db_name}....")
    for row in table_data:
        try:
            with conn:
                conn.execute(query,row)
        except sqlite3.IntegrityError as e:
                print(f"While Adding data: {row} an Error occured: {e}")
    print( f"Data Writing Completed")
    conn.close()
    return

# GET DHCP DATA FROM SH DHCP SNOOPING AND CALL the ADD FUNCTION TO UPDATE DHCP TABLE
#-----------------------------------------------------------------------------------
def expand(arg_file):
    input_line = arg_file
    match = re.search('sw\[(.*)\]_dhcp_snooping.txt',input_line)
    match_str = match.groups()[0].split('-')
    match_int = [int (x) for x in match_str]
    x_start,x_end = match_int
    x_end += 1
    host = input_line.split('[')[0]
    host_file = input_line.split(']')[1]
    full_input = [f'{host}{x}{host_file}' for x in range(x_start,x_end)]
    return full_input

def add_entry_to_dhcp_table(file_dir,my_db,dhcp_data_filename):
    base_path = file_dir
    #dhcp_data_filename = ['sw1_dhcp_snooping.txt','sw2_dhcp_snooping.txt','sw3_dhcp_snooping.txt']
    #dhcp_data_filenames = [f'{base_path}{x}' for x in dhcp_data_filename]
    sw_data_filename = 'switches.yaml'
    regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
    dhcp_table_data = []
    for file_name in dhcp_data_filename:
        sw_name,_,_ = file_name.split('_')
        open_file = f"{base_path}{file_name}"
        with open(open_file) as data:
            for line in data:
                match = regex.search(line)
                if match:
                    ox = match.groups()
                    holder = list(ox)
                    match_add_sw_active = tuple(holder + sw_name.splitlines()+[1])
                    dhcp_table_data.append(match_add_sw_active)
    dhcp_query = "replace into dhcp values (?, ?, ?, ?, ?, ?);"
    dhcp_params = {'db_name':my_db,'table_data':dhcp_table_data,'query':dhcp_query}
    add_data_to_db (**dhcp_params)
    return

#  GET SWITCH DATA FROM SWITCH.YML FILE
#--------------------------------------------------
def add_entry_to_sw_table(file_dir,my_db,sw_file):
    file_dir = str(file_dir)
    sw_dir = f'{file_dir}switches.yml'
    with open(sw_dir) as f :
        table_input = yaml.safe_load(f)
    a = table_input.values()
    x = list(a)
    sw_table_data = [ entry for entry in x[0].items()]
    sw_query =  "replace into switches values (?, ?);"
    sw_params = {'db_name':my_db,'table_data':sw_table_data,'query':sw_query}
    add_data_to_db (**sw_params)
    return

# Function call to implement the add feature
#---------------------------------------------

def add (obj):
    my_db,data_file,sw = obj.db_file,obj.filename,obj.sw_true
    dhcp = True
    file_dir = obj.file_dir
#def add(file_dir,data_file,my_db,sw=False,dhcp = True):
    db_exists = os.path.exists(my_db)
    if not db_exists:
        print("The database does not exist. Before adding data, you need to create it Using the Create_db.py file")
        return
    if sw:
        sw_file = data_file[0]
        add_entry_to_sw_table(file_dir,my_db,sw_file)
    elif  '[' in data_file[0]:
        #print (data_file[0])
        expand_file = expand(data_file[0])
        data_file = expand_file
        add_entry_to_dhcp_table(file_dir,my_db,data_file)
    else:
        add_entry_to_dhcp_table(file_dir,my_db,data_file)
    return


#                                            Get data tables from Data 
#                        ==============================================================
def parse_arg_to_get_db (obj):
    db_filename = obj.db_file
    all_content = obj.a
    key = obj.key
    value = obj.value
    if all_content:
        key = 'all'
        query_db (db_filename,key)
        return
    elif key and value:
        query_db (db_filename,key,value)
        return
    else:
        print("Please enter two or zero  arguments or all as argument")
        return

def query_db (db_filename,key,value=True):
    query_dict = {
        'vlan'    :  'select mac, ip, vlan, interface, switch, active from dhcp where vlan = ?',
        'mac'     :  'select mac, ip, vlan, interface, switch, active from dhcp where mac = ?',
        'ip'      :  'select mac, ip, vlan, interface, switch, active from dhcp where ip = ?',
        'interface': 'select mac, ip, vlan, interface, switch, active from dhcp where interface = ?',
        'switch':    'select mac, ip, vlan, interface, switch, active from dhcp where switch = ?',
        'active':    'select mac, ip, vlan, interface, switch, active from dhcp where active = ?',
        'all':       'select * from dhcp'
        }
    conn = sqlite3.connect(db_filename)
    keys = query_dict.keys()
    #conn.row_factory = sqlite3.Row
    if key not in keys:
        del query_dict['all']
        print ('Valid parameter values:  {}'.format(', '.join(keys)))
        return
    elif key == 'all':
        query = query_dict[key]
        result_generator = conn.execute(query)
        print("The dhcp table has the following entries: ")
        print ('-' * 20,'-' *12,'-'*8,'-' * 20,'-'*10,'-'*4)
        print ('{0:<20} {1:<16} {2:<8} {3:<20}{4:<6} {5:<6}\n'.format('mac address','ip address','vlan','Interface','switch','active'))
        result = list(result_generator)
        active =[row for row in result if 1 in row]
        inactive =[row for row in result if 0 in row]
        if active:
            print("Active entries")
            print ('-' * 20,'-' *12,'-'*8,'-' * 20,'-'*10,'-'*4)
            for row in active:
                print ('{0:<20} {1:<16} {2:<8} {3:<20} {4:<6} {5:<6}'.format(row[0],row[1],row[2],row[3],row[4],row[5]))
        if inactive:
            print("\nInactive entries")
            print ('-' * 20,'-' *12,'-'*8,'-' * 20,'-'*10,'-'*4)
            for row in inactive:
                print ('{0:<20} {1:<16} {2:<8} {3:<20} {4:<6} {5:<6}'.format(row[0],row[1],row[2],row[3],row[4],row[5]))


    else:
        query = query_dict[key]
        result_generator = conn.execute(query,(value,))
        result = list(result_generator)
        active =[row for row in result if 1 in row]
        inactive =[row for row in result if 0 in row]
        print(f"Information about devices with the following parameters: {key} {value}")
        print ('-' * 20,'-' *12,'-'*8,'-' * 20,'-'*10,'-'*4)
        print ('{0:<20} {1:<16} {2:<8} {3:<20}{4:<6} {5:<6}\n'.format('mac address','ip address','vlan','Interface','switch','active'))
        if active:
            print("Active entries")
            print ('-' * 20,'-' *12,'-'*8,'-' * 20,'-'*10,'-'*4)
            for row in active:
                print ('{0:<20} {1:<16} {2:<8} {3:<20} {4:<6} {5:<6}'.format(row[0],row[1],row[2],row[3],row[4],row[5]))
        if inactive:
            print("\nInactive entries")
            print ('-' * 20,'-' *12,'-'*8,'-' * 20,'-'*10,'-'*4)
            for row in inactive:
                print ('{0:<20} {1:<16} {2:<8} {3:<20} {4:<6} {5:<6}'.format(row[0],row[1],row[2],row[3],row[4],row[5]))

    conn.close()
    return



