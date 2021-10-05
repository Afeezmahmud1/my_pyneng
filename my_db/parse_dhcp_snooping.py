import parse_dhcp_snooping_functions as pds
import argparse
#pds.create_db('dhcp_snooping_schema.sql')

#add(file_dir,my_db,dhcp_data_file,sw_file='switch.yml',sw=False,dhcp = True):
#pds.add(file_dir='new_folder/',my_db='dhcp_snooping.db',dhcp_data_file= ['sw1_dhcp_snooping.txt','sw2_dhcp_snooping.txt','sw3_dhcp_snooping.txt'],sw_file='switch.yml',sw=False,dhcp = True)

#pds.parse_arg_to_get_db()
DFLT_DB_NAME = 'dhcp_snooping.db'
DFLT_DB_SCHEMA = 'dhcp_snooping_schema.sql'
DFLT_DIR = 'DATABASE'

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands',description='valid subcommands',help='description')

create_parser = subparsers.add_parser('create_db', help='create new db')
create_parser.add_argument('-n', metavar='db-filename', dest='name',default=DFLT_DB_NAME, help='db filename')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,help='db schema filename')
create_parser.set_defaults(func=pds.create_db)

add_parser = subparsers.add_parser('add', help='add data to db')
add_parser.add_argument('-d',dest='file_dir',default='folder/',help='source file base directory e.g folder/')
add_parser.add_argument('filename', nargs='+', help='file(s) to add to db')
add_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
add_parser.add_argument('-s', dest='sw_true', action='store_true',help='add switch data if set, else add normal data')
add_parser.set_defaults(func=pds.add)
#pds.add(file_dir = args.file_dir,data_file=args.filename,my_db=args.db_file,sw=args.sw_true)

get_parser = subparsers.add_parser('get', help='get data from db')
get_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
get_parser.add_argument('-k', dest="key",choices=['mac', 'ip', 'vlan', 'interface', 'switch'],help='host key (parameter) to search')
get_parser.add_argument('-v', dest="value", help='value of key')
get_parser.add_argument('-a', action='store_true', help='show db content')
get_parser.set_defaults(func=pds.parse_arg_to_get_db)

if __name__ == '__main__':
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args)



