from pprint import pprint
import asyncio
import yaml
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException
#from async_timeout import timeout
from itertools import repeat
async def send_show (device, show_commands,parsed=None):
    cmd_dict = {}
    if isinstance(show_commands,str):
        show_commands = [show_commands]
    try :
        async with AsyncScrapli ( ** device) as ssh:
            for cmd in show_commands:
                reply = await ssh.send_command (cmd)
                if parsed:
                    parsed_data = reply . textfsm_parse_output ()
                    cmd_dict[cmd] = parsed_data
                else:
                    cmd_dict [cmd] = reply.result
            return cmd_dict
    except ScrapliException as error:
        print (error, device [ "host" ])
    except:
        print (f"error connecting to  {device['host']}")
async def send_command_to_devices (devices, commands):
    show_output = []
    #coroutines = [send_show (device, commands) for device in devices]
    coroutines = map(send_show,devices,repeat(commands))

    #show_output = await asyncio.gather(*coroutines,return_exceptions=True)

    for coroutine in asyncio.as_completed (coroutines):
        result = await coroutine
        show_output.append(result)

    return show_output

if __name__ == "__main__" :
    with open ( "devices_async.yaml" ) as f:
        devices = yaml . safe_load (f)
    cmd = 'show clock'
    cmd_list = ['show clock','sh cdp nei']
    result = asyncio.run (send_command_to_devices (devices, cmd_list ))
    pprint (result, width = 120 )


