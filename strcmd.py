"""  Assignment1 """
'''
Use the click python package to build a command line tool with the following behavior.
The sample usage session should tell you all the options, arguments and subcommands that you need to define and implement.

C:\Python27\python.exe C:/work/appscourse/djangoproject/strcmd.py
Usage: strcmd.py [OPTIONS] COMMAND [ARGS]...

  Supports some string commands from command
  line

Options:
  --removedigits / --no-removedigits
                                  remove digits
                                  from input
  --help                          Show this
                                  message and
                                  exit.

Commands:
  concat  concatenates passed in strings with
          delimiter
  lower   converts the word to lower case
  upper   converts the word to upper case

Process finished with exit code 0

C:\work\appscourse\djangoproject>strcmd.py concat --help

Usage: strcmd.py concat [OPTIONS] [TOKENS]...

  pass one or more strings, concat them with delimiter  and print them out

Options:
  -d, --delimiter TEXT  defaults to :
  --help                Show this message and exit.

>strcmd.py --removedigits concat one1 two2 3three
one:two:three

>strcmd.py --removedigits concat -d , one1 two2
one,two

>strcmd.py --removedigits upper Hello12There12
HELLOTHERE

>strcmd.py upper Hello12There12
HELLO12THERE12
'''

import click

def remove_digits(str):
    #str.encode(encoding="ascii")
    return "".join([char for char in str if char.isdigit() != True])

####### another type of implementation #######
'''
class Config(object):
        def __init__(self):
            self.removedigits=False

pass_removedigits = click.make_pass_decorator(Config,ensure=True)

@click.group()
@click.option("--removedigits/--no-removedigits",default=False,help="removes digits from input")
@pass_removedigits
def cli(config,removedigits):
    """Supports some string commands from command line"""
    config.removedigits = removedigits

@cli.command()
@click.argument("input_string",nargs=1)
@pass_removedigits
def upper(config,input_string):
    if config.removedigits:
       #input_string.encode(encoding="ascii")
       input_string = remove_digits(input_string)

    click.echo(input_string.upper())


@cli.command()
@click.argument("input_string", nargs=1)
@pass_removedigits
def lower(config, input_string):
    if config.removedigits:
        #input_string.encode(encoding="ascii")
        input_string = remove_digits(input_string)

    click.echo(input_string.lower())



@cli.command()
@click.option("-d","--delimiter",default=":")

############# or ###########
###########       @click.option("--delimiter","delimit",default=":")    ############

@click.argument("input_strings",nargs=-1)
@pass_removedigits
def concat(config,delimiter,input_strings):
    if config.removedigits:
       input_strings = [remove_digits(string) for string in input_strings ]

    click.echo(delimiter.join(input_strings))

"""
@click.option("-d","--delimiter","--ravi","--teja",default=":")
### giving multiple parameter names, the option name which comes last should be passed as the parameter name
"""

'''

@click.group()
@click.option("--removedigits/--no-removedigits",default=False,help="removes digits from input")
@click.pass_context
def cli(ctx , removedigits):
    """Supports some string commands from command line"""
    ctx.obj['REMOVEDIGITS']= removedigits


@cli.command()
@click.argument("input_string",nargs=1)
@click.pass_context
def upper(ctx,input_string):
    "converts the word to upper case"
    if ctx.obj["REMOVEDIGITS"]:
       input_string = remove_digits(input_string)

    click.echo(input_string.upper())


@cli.command()
@click.argument("input_string", nargs=1)
@click.pass_context
def lower(ctx, input_string):
    "converts the word to lower case"
    if ctx.obj["REMOVEDIGITS"]:
        input_string = remove_digits(input_string)

    click.echo(input_string.lower())



@cli.command()
@click.option("-d","--delimiter",default=":")

############# or ###########
###########       @click.option("--delimiter","delimit",default=":")    ############

@click.argument("input_strings",nargs=-1)
@click.pass_context
def concat(ctx,delimiter,input_strings):
    "concatenates passed in strings with delimiter"
    if ctx.obj["REMOVEDIGITS"]:
       input_strings = [remove_digits(string) for string in input_strings ]

    click.echo(delimiter.join(input_strings))

'''
@click.option("-d","--delimiter","--ravi","--teja",default=":")
### giving multiple parameter names, the option name which comes last should be passed as the parameter name
'''


if __name__=="__main__":
    cli(obj={})