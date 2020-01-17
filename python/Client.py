#
# Client based on coroutine of asyncio
#
# LINKS
# - http://www.drdobbs.com/open-source/the-new-asyncio-in-python-34-servers-pro/240168408
# 
# NOTES
# - python3 required
#
# EE Mar '17


import asyncio, sys
 
class Client(object):
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port
        self.res = ""
        pass
    

    @asyncio.coroutine
    def simple_client(self, msg):
        # Open a connection and write a few lines by using the StreamWriter object
        reader, writer = yield from asyncio.open_connection(self.IP, self.port)

        # reader is a StreamReader object
        # writer is a StreamWriter object
        writer.write(bytes(msg+'\n','utf8'))
        
        # Now, read a single line by using the StreamReader object
        line = yield from reader.readline()
        #print(line)
        writer.close()
        self.res = line
     
    def Send(self, msg):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.simple_client(msg))
        return self.res

if len(sys.argv) >= 2:

    cl = Client(IP="172.17.0.2", port=2222)
    res = str(cl.Send(" ".join(sys.argv[1:])),'utf8')
    # remove b' and \n'
    res = res.replace("b'","")
    res = res.replace("'","")
    res = res.replace('\n','')
    print(res)
