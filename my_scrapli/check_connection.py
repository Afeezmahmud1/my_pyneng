import asyncio
from datetime import datetime
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException
from async_timeout import timeout
import yaml

class CheckConnection :
    def __init__ ( self , device_list):
        self . device_list = device_list
        self . _current_device = 0
    async def _scan_device ( self , device):
        ip = device [ "host" ]
        try:
            async with timeout ( 5 ): # for asynctelnet
                async with AsyncScrapli ( ** device) as conn:
                    prompt = await conn . get_prompt ()
                    return True , prompt
        except (ScrapliException, asyncio.TimeoutError) as error:
            return False , f"{ error } { ip }"
        except:
            return False,f'error connecting to {ip}'
    async def __anext__ ( self ):
        if self._current_device >= len ( self.device_list):
            raise StopAsyncIteration
        device_params = self . device_list [ self . _current_device]
        scan_results = await self._scan_device (device_params)
        self._current_device += 1
        return scan_results
    def __aiter__ ( self ):
        return self

class CheckConnectionPing (CheckConnection):
    def __init__ ( self , device_list):
        self . device_list = device_list
        self . _current_device = 0
    async def _scan_device ( self , device):
        reply = await asyncio . create_subprocess_shell (
                                                         f"ping -c 3 -n { device } " ,
                                                         stdout = asyncio.subprocess.PIPE,
                                                         stderr = asyncio.subprocess.PIPE,
                                                        )
        stdout, stderr = await reply.communicate ()
        output = (stdout + stderr).decode ( "utf-8" )
        if reply.returncode == 0 :
             return True , output
        else :
             return False , output

async def scan (devices, protocol):  # for ssh and telnet
    protocol_class_map = {
                              "ssh" : CheckConnection,
                              "telnet" : CheckConnection,
                              "icmp" : CheckConnectionPing,
                             }
    ConnectionClass = protocol_class_map.get (protocol.lower ())
    if ConnectionClass:
        check = ConnectionClass (devices)
        async for status, msg in check: #this call aiter(check) and anext () for each loop
            if status:
                print ( f"{ datetime.now () } { protocol } . Connection successful: { msg } " )
            else :
                print ( f"{ datetime.now () } { protocol } . Failed to connect: { msg } " )
    else :
        raise ValueError ( f"There is no corresponding class for the { protocol } " )

async def main (): # for both telnet and ssh
    with open ( "devices_async_ssh.yaml" ) as f:
         devices_ssh = yaml . safe_load (f)
    with open ( "devices_async_telnet.yaml" ) as f:
        devices_telnet = yaml . safe_load (f)
    ip_list = [ "10.2.2.13" , "10.2.2.11" , "10.1.1.1" ]
    await asyncio . gather (scan (devices_ssh, "SSH" ), scan (devices_telnet, "Telnet") , scan (ip_list, "ICMP" ))

if __name__ == "__main__" : # for ssh and telnet protocol
    asyncio.run (main ())




