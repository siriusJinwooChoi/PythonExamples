import socket

user = None
debug = False
host = '127.0.0.1'
port = 9629
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
#print(s.recv(1024))
#s.close
cmd_request = {'.user': 'USER %s\r\n',
        '.list' : 'LIST \r\n',
        '.quit' : 'QUIT \r\n',
        '.debug' : None,
        }
def parseCommand(ui):
    "Parse a user command and return the request message"
    global user, debug, requestmsg

    words = ui.split()
    #if empty or first word is is not keyword, this is FROM message
    if not words or words[0] not in cmd_request:
        requestmsg = "FROM %s:%s \r\n" %(user,ui)
        s.send(requestmsg)
        #return "FROM %s:%s\r\n" % (user, ui)
    cmd = words[0]
    if (cmd == '.user' and len(words) != 2) or \
       (cmd != '.user' and len(words) != 1):
        print('Syntax error')
        return None
    if cmd == '.debug':
        debug = False if debug else True
        print('Debug %s' % debug)
        return None
    if cmd == '.user':
        user = words[1]
        return cmd_request[cmd] % user
        s.send(cmd_request[cmd] % user)
    elif cmd == '.list':
        s.send(cmd_request[cmd] + user)
    elif cmd == '.quit':
        s.send(cmd_request[cmd])
        s.close()
    else:
        print('Illegal command.\n')
    #return cmd_request[cmd]

def runRequest():
    "Get user commands and generate request messages"
    while True: 
        ui = input('>> ')
        requestMsg = parseCommand(ui)
        if requestMsg is not None:
            print(requestMsg)
    #pass

if __name__ == "__main__":
    runRequest()
    '''if len(sys.argv) == 3:
        serverHost = sys.argv[1]
        serverPort = int(sys.argv[2])
    else:
        print('Usage: {} <ipaddress> <port>'.format(sys.argv[0]), file=sys.stderr)
        exit(1)
    #debug = True
    runRequest()'''