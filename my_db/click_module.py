import click

#'''
#@click.group()
##@click.option('--debug/--no-debug', default=False)
#def cli(debug):
#
#@click.command()
#@click.option('--count', default=1, help='Number of greetings.')
#@click.option('--name', prompt='Your name',
#              help='The person to greet.')
#def hello(count, name):
#    """Simple program that greets NAME for a total of COUNT times."""
#    for x in range(count):
#        click.echo(f"Hello {name}!")
#'''
@click.group()
def cli():
    pass

@cli.command(name='create')
@cli.option('--db-name', default='dhcp_snooping.db', help='database file name.')
def initdb(db_name):
    click.echo('Initialized the database')
    click.echo(f'{db_name} DB was created succesfully')

@cli.command(name='delete')
def dropdb():
    click.echo('Dropped the database')
if __name__ == '__main__':
    cli()
