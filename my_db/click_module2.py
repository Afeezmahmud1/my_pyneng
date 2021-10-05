import click

@click.group()
def messages():
  pass


@click.command()
@click.option('--db-name', default='dhcp_snooping.db', help='database file name')
@click.option('--admin',help= 'Database Admin')
def generic(db_name,admin):
    my_name = add_hyphen(admin)
    click.echo(f'Congratulation!! {my_name} you have successfully created {db_name} db ')

def add_hyphen (f_name):
    n_name = list(f_name)
    s_name = '-'.join(n_name)
    return s_name
@click.command()
def welcome():
    click.echo('Welcome')


messages.add_command(generic,name='add')
messages.add_command(welcome)

if __name__ == "__main__":
    messages()
