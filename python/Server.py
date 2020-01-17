#
# Server based on coroutine of asyncio
#
# LINKS
# - http://www.drdobbs.com/open-source/the-new-asyncio-in-python-34-servers-pro/240168408
# 
# NOTES
# - python3 required
#
# EE Mar '17

import asyncio
# REPLACE
from fas import Fas
from datetime import datetime

class Server(object):
    def __init__(self):
        # [REPLACE]
        # Fas object
        self.fas = Fas()
        print('Fas object created.')
        pass

    @asyncio.coroutine
    def simple_server(self):
        # Start a socket server, call back for each client connected.
        # The client_connected_handler coroutine will be automatically converted to a Task
        yield from asyncio.start_server(self.client_connected_handler, host='0.0.0.0', port=2222, limit=2**20)
 
    @asyncio.coroutine
    def client_connected_handler(self, client_reader, client_writer):
        # Runs for each client connected
        # client_reader is a StreamReader object
        # client_writer is a StreamWriter object
        #print("Connection received!")
        while True:
            data = yield from client_reader.readline()
            if not data:
                break
            print(str(datetime.now()))
            #print(data[1:20])
            message = str(data, 'utf8')
            
            # [REPLACE]
            # message: comma separated fields: first one function, rest corresponding arguments
            result = self.fas.MessageHandler(message)
            
            print(result)
            client_writer.write(bytes(result+'\n', 'utf8'))

    def Start(self): 
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.simple_server())
        try:
            loop.run_forever()
        finally:
            loop.close()


sv = Server()
sv.Start()
