import socket
import select

host = ''
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)
conn, addr = sock.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])
while 1:
    data = conn.recv(1024)
    print data
s.close() 
