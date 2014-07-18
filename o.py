#!/usr/bin/env python

'''


pip install flask Flask-HTTPAuth

'''

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
 
app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()
 
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
    
def make_circuit_metrics(id, latency, throughput):
    new_metrics = {}
    new_metrics['id'] = id
    new_metrics['latency'] = latency
    new_metrics['throughput'] = throughput
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
    '''
    # Call OVSDB json-rpc  to configure TEP
  
    rpc_ovsdb_create_tep()	
    Compute node:
    start_ip = 192.168.1.182
    end_ip = 192.168.1.183

    ovs-vsctl add-br isolated0
    ifconfig isolated0 192.168.222.2 up
    ovs-vsctl -vjsonrpc add-port isolated0 gre0 -- set interface gre0 type=gre options:remote_ip=10.36.0.134
    # ovs-vsctl add-port isolated0 vxlan -- set interface vxlan type=vxlan options:key=10 options:local_ip=192.168.222.1 options:remote_ip=10.36.0.133
    ovs-vsctl del-port br-eth2 eth2
    ovs-vsctl add-port isolated0 eth2
    ping -I isolated0 192.168.222.1

    ovs-vsctl add-br isolated0
    ifconfig isolated0 192.168.222.1 up
    ovs-vsctl -vjsonrpc add-port isolated0 gre0 -- set interface gre0 type=gre options:remote_ip=10.36.0.133
    # ovs-vsctl add-port isolated0 vxlan -- set interface vxlan type=vxlan options:key=10 options:local_ip=192.168.222.2 options:remote_ip=10.36.0.134
    ovs-vsctl del-port br-eth2 eth2
    ovs-vsctl add-port isolated0 eth2
    ping -I isolated0 192.168.222.2

    json-rpc client call
    rpc_faultmonitor_start(id, start_ip_address, end_ip_address);

    '''
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
    print "Create circuit"
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    print "Find circuit"
    if len(circuit) == 0:
        abort(404)
    print "Validate circuit data"
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
    print "Update circuit data"
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
    circuits.remove(circuit[0])
    return jsonify( { 'status':'ok','result': circuit[0]['id'] } )
    
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
    return jsonify( { 'status':'ok', 'result': true } )
    
@app.route('/compute/api/v1.0/performancemetrics/<int:circuit_id>', methods = ['GET'])
# @auth.login_required
def compute_performance_metrics_get(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    return jsonify( { 'status':'ok', 'metrics': make_circuit_metrics(circuit_id, latency, throughput) } ), 201
    
'''
Not needed at the moment ovsdb

@app.route('/compute/api/v1.0/circuits', methods = ['POST'])
# @auth.login_required
def compute_circuit_create():
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
    return jsonify( { 'status':'ok', 'result':circuit['id'], 'circuit': make_circuits(circuits) } ), 201
'''

    
if __name__ == '__main__':
    app.run('0.0.0.0', 5555, debug=True)


'''
Request methods using CURL:
 
0. curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/hello

1. curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/circuits
 
2. curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/circuits/2
 
3. curl -i -u user:password -H "Content-Type: application/json" -X POST -d '{ "service_type": "epl", "start_ip_address": "192.168.1.3", "end_ip_address": "192.168.1.4", "classifier": "red", "self": "http://localhost:8888/service_id/1" }' http://localhost:5555/orchestrator/api/v1.0/circuits

4. curl -i -u user:password -H "Content-Type: application/json" -X PUT -d '{ "id": 1, "service_type": "epl", "start_ip_address": "192.168.1.3", "end_ip_address": "192.168.1.4", "classifier": "blue", "self": "http://localhost:8888/service_id/1", "active": true }' http://localhost:5555/orchestrator/api/v1.0/circuits/1

5. curl -i  -H "Content-Type: application/json" -X PUT -d '{"start_ip_address":"2.2.2.2","self":"http://local/1","end_ip_address":"1.1.1.1","service_type":"vepl","classifier":"11","active":true}' http://localhost:5555/orchestrator/api/v1.0/circuits/1

6. curl -i  -H "Content-Type: application/json" -X PUT -d '{"active":true}' http://localhost:5555/orchestrator/api/v1.0/circuits/1

7. curl -i -u user:password http://localhost:5555//orchestrator/api/v1.0/performancemetrics/2

8. curl -i -u user:password  -H "Content-Type: application/json" -X DELETE http://localhost:5555/orchestrator/api/v1.0/circuits/2

9. curl -i  -H "Content-Type: application/json" -X PUT -d '{"active":true}' http://localhost:5555/debug
 
'''

