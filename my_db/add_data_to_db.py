import os
import yaml
from pprint import pprint
import re
import sqlite3

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
#==========================================================================================
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


#GET SWITCH DATA FROM SWITCH.YML FILE
#======================================
def add_entry_to_sw_table(file_dir,my_db,sw_file):
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

def add(file_dir,my_db,dhcp_data_file,sw_file='switch.yml',sw=False):
    db_exists = os.path.exists(my_db)
    if not db_exists:
        print("The database does not exist. Before adding data, you need to create it Using the Create_db.py file")
        return
    if sw:
        add_entry_to_sw_table(file_dir,my_db,sw_file)
    add_entry_to_dhcp_table(file_dir,my_db,dhcp_data_file)
    return



#USE ADD_DATA_TO_DB FUNCTION TO ADD DATA TO TABLES IN DATABASE
#================================================================
if __name__ == "__main__":
    func_params= {'file_dir':'new_folder/',
                   'my_db':'dhcp_snooping.db',
                   'dhcp_data_file':['sw1_dhcp_snooping.txt','sw2_dhcp_snooping.txt','sw3_dhcp_snooping.txt'],
                   'sw_file':'switch.yml',
                   'sw':False
                 }
    add(**func_params)
    
    #sw_query =  "insert into switches (hostname, location) values (?, ?)"
    #dhcp_query = "replace into dhcp values (?, ?, ?, ?, ?, ?);"
    #sw_params = {'db_name':my_db,'table_data':sw_table_data,'query':sw_query}
    #dhcp_params = {'db_name':my_db,'table_data':dhcp_table_data,'query':dhcp_query}
    #add_data_to_db (**sw_params)
    #add_data_to_db (**dhcp_params)





