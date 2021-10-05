import sqlite3
import yaml
import os
import re
import sys
from pprint import pprint
def parse_arg_to_get_db (db_filename = 'dhcp_snooping.db'):
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == 'all'):
        key = 'all'
        query_db (db_filename,key)
        return
    elif len(sys.argv) == 3:
        key,value = sys.argv[1:]
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
if __name__ == "__main__":
    parse_arg_to_get_db()

