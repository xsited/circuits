import sys
import re
import subprocess
import json
import commands

def getmac(iface):
    ifconfig = commands.getoutput("ifconfig " + iface)
    mac = re.search('\w\w:\w\w:.+\n', ifconfig)
    if mac is None:
        #parsedMac = 'Mac not found'
        parsedMac = 'None'
    else:
        parsedMac = mac.group().rstrip()
    return parsedMac #Or use return here.

#bring on new module
#def test_netiface(iface='eth0'):
#    from netifaces import interfaces, ifaddresses, AF_INET
#    for ifaceName in interfaces():
#         addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
#         print '%s: %s' % (ifaceName, ', '.join(addresses))

def getip(iface='eth0'):
    import socket, fcntl, struct
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd = sock.fileno()
    SIOCGIFADDR = 0x8915
    
    ifreq = struct.pack('16sH14s', iface.encode('utf-8'), socket.AF_INET, b'\x00'*14)
    try:
        res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
    except:
        return None
    ip = struct.unpack('16sH2x4s8x', res)[2]
    return socket.inet_ntoa(ip)
    
def get_network_all_json():
    lines = open("/proc/net/dev", "r").readlines()

    columnLine   = lines[1]

    # here you can use a list slice (the "[1:3]") to 
    # capture only the bits you want...
    receiveCols, transmitCols = columnLine.split("|")[1:3]  

    receiveCols  = map(lambda a:"recv_"+a,  receiveCols.split())
    transmitCols = map(lambda a:"trans_"+a, transmitCols.split())

    cols = receiveCols+transmitCols

    faces = {}
    if_list = [];
    for line in lines[2:]:
          if line.find(":") < 0: 
                continue
          face, data  = line.split(":")
	  face = face.rstrip().lstrip();
	  if_list.append(face);
          faceData    = dict(zip(cols, data.split()))
          faces[face] = faceData
    	  #print "JSON: ", face, json.dumps(faces[face], indent=4)
    #print "JSON: ", json.dumps(faces, indent=4)
    #uncomment the following line for a "prettier" output
    #print("JSON: "+ json.dumps(faces, indent=4))
    #print("ifaces: ", if_list)
    return (if_list, faces)


def get_network_bytes(interface):
    for line in open('/proc/net/dev', 'r'):
        if interface in line:
            data = line.split('%s:' % interface)[1].split()
            rx_bytes, tx_bytes = (data[0], data[8])
            return (rx_bytes, tx_bytes)

def main():
    if_list, faces = get_network_all_json()
    #print("JSON: "+ json.dumps(faces, indent=4))
    #print("LIST:  ", if_list)
    #print("JSON: "+ json.dumps(faces['eth0'], indent=4))
    
    for i in if_list:
    	print "iface : ", i.rstrip().lstrip()
    	print "MAC   : ", getmac(i)
        print "IP    : ", getip(i)
	print "DATA  : " 
        print json.dumps(faces[i], indent=4)
    	print "======================"

    rx_bytes, tx_bytes = get_network_bytes('eth0')
    print '%s bytes received' % rx_bytes
    print '%s bytes sent' % tx_bytes
    #test_netiface()
    #sys.exit(0)

if __name__ == '__main__':
    main()

