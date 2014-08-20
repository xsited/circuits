#!/usr/bin/env python

'''
'''

__author__ = 'xsited'
import os
import sys
import json
import argparse
import datetime
import socket
import threading
import select
from time import time, sleep, ctime
from collections import deque
from restapi import OClient

import subprocess as subps

try:
    from flask import Flask, jsonify, abort, request, make_response, url_for
except ImportError:
    print 'You will need the Flask python module installed to use this script'
    print 'You can install it using the following command'
    print 'sudo pip install Flask'
    sys.exit(1)

try:
    from flask.ext.httpauth import HTTPBasicAuth
except ImportError:
    print 'You will need the HTTPBasicAuth python module installed to use this script'
    print 'You can install it using the following command'
    print 'sudo pip install Flask-HTTPAuth'
    sys.exit(1)


try:
    import daemonize
except ImportError:
    daemonize = None
 
try:
    import ping
except ImportError:
    ping = None
    print 'You will need the ping python module installed to use this script'
    print 'You can install it using the following command'
    print 'sudo pip install ping'
    sys.exit(1)


class oTimeout(Exception):
    pass

class oError(Exception):
    pass
 

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()
oc = OClient()
pthread = threading.Thread()

@auth.get_password
def get_password(username):
    if username == 'user':
        return 'password'
    return None
 
@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

latency = 35
throughput = 100

circuits = [
{  
   'id': 1,
   'service_type': 'epl', 
   'start_ip_address': u'192.168.1.1', 
   'end_ip_address': u'192.168.1.2',
   'classifier': u'12',
   'active': False,
   'self': 'uri'
},
{  
   'id': 2,
   'service_type': 'epl', 
   'start_ip_address': u'192.168.1.3', 
   'end_ip_address': u'192.168.1.4',
   'classifier': u'red',
   'active': False,
   'self': 'uri'
},

]
 


def c_circuit_delete(circuit_id,start_ip, end_ip, circuit_type='gre'):
    if circuit_type == 'gre':
        ovscfg_sh = '\
#!/bin/bash\n\n\
ovs-vsctl del-port gre0 \n\
'

    else:
        ovscfg_sh = '\
#!/bin/bash\n\n\
ovs-vsctl del-port vxlan \n\
'

    with open('/tmp/ovscfg.sh', 'w') as f:
    	f.write(ovscfg_sh)

    cmd = "/bin/bash /tmp/ovscfg.sh" # %s %s" % (data_start_ip, data_end_ip)
    if subps.call(cmd.split(), stderr=file('ovscfg.err', 'w')):
        raise oError()


    
def c_circuit_add(circuit_id,start_ip, end_ip, circuit_type='gre'):
    '''
    Configure circuit can be confgured at a couple different ReSTful RPC levels
    Option 1:
	Custom RPC - Call a custom RPC to configure the circuit
    Option 2:
    	Call OVSDB json-rpc  ovsdb.py is a PoC of this interface
    Option 3:
	ODL ReSTful NB rpc (which calls SB ODL OVSDB) -  need example
    Option 4:
	Openstack Neutron ML2 rpc - need example

    circuit_type currently is an enum of possibile implmenetation types
    gre
    vxlan
    
  
    The endpoints should be addressed by management interfaces so status reporting is possble when link is down
    start_ip = 10.0.0.133
    end_ip = 10.0.0.134
    '''

    mylist = start_ip.split(".",4)
    start_host = mylist[3]
    print "start_host = %s" % start_host
    mylist = end_ip.split(".",4)
    end_host = mylist[3]
    print "end_host = %s" % end_host
    tunnel_start_ip="192.168.222." + start_host
    print "tunnel_start_ip = %s" % tunnel_start_ip
    tunnel_end_ip="192.168.222." + end_host
    print "tunnel_end_ip = %s" % tunnel_end_ip
    data_start_ip="10.36.0." + start_host
    print "data_start_ip = %s" % data_start_ip
    data_end_ip="10.36.0." + end_host
    print "data_end_ip = %s" % data_end_ip
     

    print "Remote Server = ", end_ip

     
    '''
    This is the tunnel addressing assumed configuration
    ovs-vsctl add-br isolated0
    #ifconfig isolated0 192.168.222.133 up
    ifconfig isolated0 tunnel_start_ip up
    # steal eth2 from default openstack configuration (optional and internal note)
    # ovs-vsctl del-port br-eth2 eth2

    # ovs-vsctl add-port isolated0 eth2
    cpe_interface='gre0'
    ovs-vsctl add-port isolated0 cpe_interface
    '''
 
    if circuit_type == 'gre':
        ovscfg_sh = '\
#!/bin/bash\n\
S=$1\n\
R=$2\n\
ovs-vsctl del-port gre0 \n\
ovs-vsctl add-port isolated0 gre0 -- set interface gre0 type=gre options:remote_ip=$R\n\
'

          #ovs-vsctl -vjsonrpc add-port isolated0 gre0 -- set interface gre0 type=gre options:remote_ip=10.36.0.134
    else:
        ovscfg_sh = '\
#!/bin/bash\n\
S=$1\n\
R=$2\n\
ovs-vsctl del-port vxlan \n\
ovs-vsctl add-port isolated0 vxlan -- set interface vxlan type=vxlan options:key=10 options:local_ip=$L options:remote_ip=$R\n\
'

    with open('/tmp/ovscfg.sh', 'w') as f:
    	f.write(ovscfg_sh)

    #cmd = "screen -m -d /bin/bash /tmp/ovscfg.sh %s %s" % (data_start_ip, data_end_ip)
    cmd = "/bin/bash /tmp/ovscfg.sh %s %s" % (data_start_ip, data_end_ip)
    if subps.call(cmd.split(), stderr=file('ovscfg.err', 'w')):
        raise oError()

    
'''
    rpc_faultmonitor_start(circuit_id, interface, end_ip_address);
    	 # ping -I isolated0 192.168.222.134
         ping -I interface end_ip_address


    ovs-vsctl add-br isolated0
    ifconfig isolated0 192.168.222.134 up

    # steal eth2 from default openstack configuration (optional and internal note)
    # ovs-vsctl del-port br-eth2 eth2

    ovs-vsctl add-port isolated0 eth2

    if circuit_type == 'gre':
    	# ovs-vsctl -vjsonrpc add-port isolated0 gre0 -- set interface gre0 type=gre options:remote_ip=10.36.0.133
        ovs-vsctl add-port isolated0 gre0 -- set interface gre0 type=gre options:remote_ip=10.36.0.133
    else:
        ovs-vsctl add-port isolated0 vxlan -- set interface vxlan type=vxlan options:key=10 options:local_ip=192.168.222.134 options:remote_ip=10.36.0.133

    rpc_faultmonitor_start(circuit_id, interface, end_ip_address);
         # ping -I isolated0 192.168.222.133
         ping -I interface end_ip_address

'''

def print_circuit(circuit):
    print "service_type = %s" % circuit[0]['service_type']
    print "start_ip_address = %s" % circuit[0]['start_ip_address']
    print "end_ip_address = %s" % circuit[0]['end_ip_address']
    print "classifier = %s" % circuit[0]['classifier']
    print "self = %s" % circuit[0]['self']
    print "active = %s" % circuit[0]['active']


def make_public_circuit(circuit):
    new_circuit = {}
    for field in circuit:
        if field == 'id':
            new_circuit['uri'] = url_for('get_circuit', circuit_id = circuit['id'], _external = True)
        else:
#	    print "field = ",field
            new_circuit[field] = circuit[field]
    return new_circuit
  
def make_circuit_status(circuit_id, active):
    new_status = {}
    if active:
        new_status['status'] = "running"
    else:
        new_status['status'] = "suspended"

'''
JT: id is reserved
  '''
def make_circuit_metrics(circuit_id, latency, throughput):
    new_metrics = {}
    new_metrics['id'] = circuit_id
    new_metrics['latency'] = latency
    new_metrics['throughput'] = throughput
    new_metrics['latency_UnitMeasurement'] = "ms"
    new_metrics['throughput_UnitMeasurement'] = "Mbps"
    return new_metrics


@app.route('/orchestrator/api/v1.0/circuits', methods = ['GET'])
# @auth.login_required
def get_circuits():
    return jsonify( { 'circuits': map(make_public_circuit, circuits) } )
 
@app.route('/orchestrator/api/v1.0/hello', methods = ['GET'])
# @auth.login_required
def get_hello():
    return jsonify( { 'hello': 'world' } )
 
@app.route('/orchestrator/api/v1.0/circuits/<int:circuit_id>', methods = ['GET'])
# @auth.login_required
def get_circuit(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    return jsonify( { 'circuit': make_public_circuit(circuit[0]) } )
 
@app.route('/orchestrator/api/v1.0/circuits', methods = ['POST'])
# @auth.login_required
def create_circuit():
    print "Create circuit"
    print request.json
#    if not request.json : #or not 'service_type' in request.json:
#        abort(400)
    print "Build circuit"
    circuit = {
        'id': circuits[-1]['id'] + 1,
        'service_type': request.json['service_type'],
        'start_ip_address': request.json.get('start_ip_address', ""),
        'end_ip_address': request.json.get('end_ip_address', ""),
        'classifier': request.json.get('classifier', ""),
        'self': request.json.get('self', ""),
        'active': False
    }
    print "Append circuit"
    circuits.append(circuit)
    
    print "Call computes to create circuit"
    #c_circuit = dict(circuit)
    #c_circuit['self']='http://10.0.0.192:5555/orchstrator/api/v1.0/reportstatus/%d'%circuit['id']
    oc.c_circuit_create_on_server(circuit, circuit['start_ip_address'])
    oc.c_circuit_create_on_server(circuit, circuit['end_ip_address'])

    print "Return circuit"
    return jsonify( { 
	'status': 'ok',
        'id': circuit['id'],
	'circuit': make_public_circuit(circuit) 
	}
	), 201
 
@app.route('/debug', methods = ['PUT'])
# @auth.login_required
def debug():
    print "Debug circuit"
    json = request.json
    print(json)
    # Render template
    return jsonify(json)


@app.route('/orchestrator/api/v1.0/circuits/<int:circuit_id>', methods = ['PUT'])
# @auth.login_required
def update_circuits(circuit_id):

    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    print "Find circuit"
    if len(circuit) == 0:
        abort(404)
#    print "Validate circuit data"
    '''
    if not request.json:
        abort(400)
    if 'service_type' in request.json and type(request.json['service_type']) != unicode:
        abort(400)
    if 'start_ip_address' in request.json and type(request.json['start_ip_address']) is not unicode:
        abort(400)
    if 'active' in request.json and type(request.json['active']) is not bool:
        abort(400)

    '''
#    print "Update circuit data"
    print_circuit(circuit)

    '''
    print "service_type = %s" % circuit[0]['service_type']
    '''
    circuit[0]['start_ip_address'] = request.json.get('start_ip_address', circuit[0]['start_ip_address'])
    circuit[0]['self'] = request.json.get('self', circuit[0]['self'])
    circuit[0]['end_ip_address'] = request.json.get('end_ip_address', circuit[0]['end_ip_address'])
    circuit[0]['classifier'] = request.json.get('classifier', circuit[0]['classifier'])
    circuit[0]['service_type'] = request.json.get('service_type', circuit[0]['service_type'])
    circuit[0]['active'] = request.json.get('active', circuit[0]['active'])
    print "Return something "
    return jsonify( { 
	'status': 'ok',
	'result': circuit[0]['id'] ,
	'circuit': make_public_circuit(circuit[0]) 
	}
	), 201
 
    # return jsonify( { 'circuit': make_public_circuit(circuit[0]) } )
    
@app.route('/orchestrator/api/v1.0/circuits/<int:circuit_id>', methods = ['DELETE'])
# @auth.login_required
def delete_circuits(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    print "Call computes to delete circuit"
    oc.c_circuit_delete_on_server(circuit_id, circuit[0]['start_ip_address'])
    oc.c_circuit_delete_on_server(circuit_id, circuit[0]['end_ip_address'])
    circuits.remove(circuit[0])
    return jsonify( { 'status':'ok','result': circuit[0]['id'] } )
    
@app.route('/orchestrator/api/v1.0/reportmetrics/<int:circuit_id>', methods = ['PUT'])
# @auth.login_required
def report_metrics(circuit_id):
    global latency
    global throughput
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    latency = request.json.get('latency', latency)
    throughput = request.json.get('throughput', throughput)
    return jsonify( { 'status':'ok', 'result': True } )

@app.route('/orchestrator/api/v1.0/reportstatus/<int:circuit_id>', methods = ['PUT'])
# @auth.login_required
def report_status(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    tempactive = circuit[0]['active']
    s = request.json.get('status', "")
    
    if s == 'running':
	print "status ", s
        active = circuit[0]['active'] = True
    else:
	print "status ", s
        active = circuit[0]['active'] = False

    print "active ", active
    if tempactive == active:
	print "status no change"
    else:
        oc.o_report_status_self(circuit_id, circuit[0]['self'], make_circuit_status(circuit_id,circuit[0]['active']))
    return jsonify( { 'status':'ok', 'result': True } )

#@app.route('/orchestrator/api/v1.0/performancemetrics/<int:circuit_id>', methods = ['PUT'])
# @auth.login_required
#def report_metrics(circuit_id):
#    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
#    if len(circuit) == 0:
#        abort(404)
#    return jsonify( { 'status':'ok', 'result': True } )

@app.route('/orchestrator/api/v1.0/performancemetrics/<int:circuit_id>', methods = ['GET'])
# @auth.login_required
def performance_metrics_get(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    return jsonify( { 'status':'ok', 'metrics': make_circuit_metrics(circuit_id, latency, throughput) } ), 201

@app.route('/compute/api/v1.0/faultmonitor/<int:circuit_id>', methods = ['POST'])
# @auth.login_required
def compute_faultmonitor_start(circuit_id, start_ip, end_ip):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    # ping_start (end_ip);
    return jsonify( { 'status':'ok', 'result': True } )
    
@app.route('/compute/api/v1.0/performancemetrics/<int:circuit_id>', methods = ['GET'])
# @auth.login_required
def compute_performance_metrics_get(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    return jsonify( { 'status':'ok', 'metrics': make_circuit_metrics(circuit_id, latency, throughput) } ), 201
    

@app.route('/compute/api/v1.0/circuits', methods = ['POST'])
# @auth.login_required
def compute_circuit_create():
    global options
    if not request.json or not 'service_type' in request.json:
        abort(400)
    circuit = {
        'id': circuits[-1]['id'] + 1,
        'service_type': request.json['service_type'],
        'start_ip_address': request.json.get('start_ip_address', ""),
        'end_ip_address': request.json.get('end_ip_address', ""),
        'self': request.json.get('self', ""),
        'classifier': request.json.get('classifier', ""),
        'active': True
    }
    #if request.host == circuit['start_ip_address']:
    myserver = request.host.split(":",2)
    if myserver[0] == circuit['start_ip_address']:
        c_circuit_add(circuit['id'], circuit['start_ip_address'], circuit['end_ip_address'])
        #if options.pingstart:
	start_ping(circuit, circuit['end_ip_address'])
    else:
        c_circuit_add(circuit['id'], circuit['end_ip_address'], circuit['start_ip_address'])
        
    circuits.append(circuit)
    return jsonify( { 
	'status': 'ok',
        'id': circuit['id'],
	'circuit': make_public_circuit(circuit) 
	}
	), 201
 
@app.route('/compute/api/v1.0/circuits/<int:circuit_id>', methods = ['DELETE'])
# @auth.login_required
def compute_circuit_delete(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    myserver = request.host.split(":",2)
    if myserver[0] == circuit[0]['start_ip_address']:
	stop_ping()
        
    c_circuit_delete(circuit_id, circuit[0]['end_ip_address'], circuit[0]['start_ip_address'])
    circuits.remove(circuit[0])
    return jsonify( { 'status':'ok','result': circuit[0]['id'] } )
    
 


def get_root():
    print 'This script needs to run as root. Please provide your sudo password'
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    os.execlpe('sudo', *args)
    return os.getuid()


def parse_options():
    parser = argparse.ArgumentParser(prog='o.py', description='ReSTFul ochestrator to create circuit')
    parser.add_argument('-q', '--quite', action='store_true',
                        help='Quite mode, update the terminal only when there is a timeout')
    parser.add_argument('-n', '--notify', action='store_true',
                        help='Notify on')
    parser.add_argument('-c', '--compute', action='store_true',
                        help='Perform Compute role')
    parser.add_argument('-p', '--pingstart', action='store_true',
                        help='Autostart health checking on circuit create')
    parser.add_argument('-d', '--daemonize', action='store_true',
                        help='Run the process in the background as a daemon ')
    args = parser.parse_args()
    return args


    
def main():
     
    global options 
    options = parse_options()
    uid = os.getuid()
    # print 'UserID = ', uid
    if uid != 0:
        print 'Failed to get root permissions. Exiting!'
        print 'You need to run as root to set command and open raw sockets'
        print 'sudo python o.py'
        sys.exit(1)

    #   uid = get_root()
    #   if uid != 0:
    #       print 'Failed to get root permissions. Exiting!'
    #       sys.exit(1)

    if options.daemonize and not daemonize:
        print 'You do not have the necessary library run in daemon mode'
        print 'Install the library using the following command'
        print 'sudo pip install daemonize'
        sys.exit(1)

    if options.daemonize:
        options.notify = True
        daemon = daemonize.Daemonize(app='o', pid='/tmp/o.pid', action=main)
        daemon.start()
    else:
        if options.quite:
            print('Running in quite mode, will update when a timeout occurs')

    app.run('0.0.0.0', 5555, debug=True)




def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])


def showNotification(title, body):
    print title, body

# PingLoop adopted and modified from check_internet.py, Akshet Pandey argetlam [dot] akshet [at] gmail [dot] com
class PingLoop(threading.Thread):
    def __init__(self, options, circuit, endpoint):
        self.options = options
        self.circuit = circuit
        self.endpoint = endpoint
        self.loop = True
	threading.Thread.__init__(self)
        #signal.signal(signal.SIGINT, self.stopLoop)

    def stopLoop(self):
        if self.loop:
            self.loop = False
            print 'Received exit signal. Stopping!'

    #def runPingLoop(self):
    def run(self):
        delayList = deque(maxlen=100)
        lastTimeout = None
        netUp = True
        replySuccessCount = 0
        replyFailCount = 0

        # cls()
        while self.loop:
            try:
                delay = ping.do_one(self.endpoint, 3, 64)
            except socket.error:
                delay = None
            except select.error:
                delay = None

            if delay:
                delayList.append(delay)
                replySuccessCount += 1
                replyFailCount = 0
            else:
                lastTimeout = time()
                replySuccessCount = 0
                replyFailCount += 1

            if replySuccessCount >= 10 and not netUp:
                netUp = True
                if self.options.notify:
                    showNotification('Net Status', 'Net is back!')
                    if self.circuit['active'] == False:
                	self.circuit['active'] = True
			oc.o_report_status(circuit_id, make_circuit_status(circuit_id, self.circuit['active']))
            elif replyFailCount >= 10 and netUp:
                netUp = False
                if self.options.notify:
                    showNotification('Net Status', 'Net is down!')
                    if self.circuit['active'] == True:
                	self.circuit['active'] = False
			oc.o_report_status(circuit_id, make_circuit_status(circuit_id, self.circuit['active']))

            if not self.options.quite or not delay:
                # cls()
                if len(delayList):
		    global latency 
		    latency = str(sum(delayList) / len(delayList) * 1000)
                    print 'Circuit id ', self.circuit['id'], ' status of  ', self.circuit['end_ip_address'], 'Average delay of last ', len(delayList), ' pings is ', sum(delayList) / len(delayList) * 1000, ' ms'
                if not self.options.quite and lastTimeout:
                    print 'Last timeout was ', str(timedelta(seconds=time() - lastTimeout)), 'seconds ago.'
                elif lastTimeout:
                    print 'Last timeout was at ', ctime(lastTimeout)

			
                #else:

                #    print 'There has been no timeouts yet! Hurray!'
                sleep(2)


def stop_ping():
    global pingLoop
    pingLoop.stopLoop()
    # pingLoop.cancel()

def start_ping(circuit, end_ip):
    global pingLoop
    pingLoop = PingLoop(options, circuit, end_ip)
    pingLoop.start()


if __name__ == '__main__':
    main()

#if __name__ == '__main__':
#    app.run('0.0.0.0', 5555, debug=True)


'''
Request methods using CURL:
 
0. curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/hello

1. curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/circuits
 
2. curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/circuits/2
 
3. curl -i -u user:password -H "Content-Type: application/json" -X POST -d '{ "service_type": "epl", "start_ip_address": "192.168.1.3", "end_ip_address": "192.168.1.4", "classifier": "red", "self": "http://localhost:8888/service_id/1" }' http://localhost:5555/orchestrator/api/v1.0/circuits

4. curl -i -u user:password -H "Content-Type: application/json" -X PUT -d '{ "id": 1, "service_type": "epl", "start_ip_address": "192.168.1.3", "end_ip_address": "192.168.1.4", "classifier": "blue", "self": "http://localhost:8888/service_id/1", "active": true }' http://localhost:5555/orchestrator/api/v1.0/circuits/1

5. curl -i  -H "Content-Type: application/json" -X PUT -d '{"start_ip_address":"2.2.2.2","self":"http://local/1","end_ip_address":"1.1.1.1","service_type":"vepl","classifier":"11","active":true}' http://localhost:5555/orchestrator/api/v1.0/circuits/1

6. curl -i  -H "Content-Type: application/json" -X PUT -d '{"active":true}' http://localhost:5555/orchestrator/api/v1.0/circuits/1

7. curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/performancemetrics/2

8. curl -i -u user:password  -H "Content-Type: application/json" -X DELETE http://localhost:5555/orchestrator/api/v1.0/circuits/2

9. curl -i  -H "Content-Type: application/json" -X PUT -d '{"active":true}' http://localhost:5555/debug


 
'''

