#!/usr/bin/env python

'''




'''

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
 
app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()
 
@auth.get_password
def get_password(username):
    if username == 'user':
        return 'python'
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

circuits = [
{  
   'id': 1,
   'service_type': 'epl', 
   'start_ip_ address': u'192.168.1.1', 
   'end_ip_address': u'192.168.1.2',
   'classifier': u'12',
   'active': False
},
{  
   'id': 2,
   'service_type': 'epl', 
   'start_ip_ address': u'192.168.1.3', 
   'end_ip_address': u'192.168.1.4',
   'classifier': u'red',
   'active': False
},

]
 

def make_circuit(circuit):
    new_circuit = {}
    for field in circuit:
        if field == 'id':
            new_circuit['uri'] = url_for('get_circuit', circuit_id = circuit['id'], _external = True)
        else:
            new_circuit[field] = circuit[field]
    return new_circuit
    
@app.route('/orchestrator/api/v1.0/circuit', methods = ['GET'])
# @auth.login_required
def get_circuits():
    return jsonify( { 'circuits': map(make_circuit, circuits) } )
 
@app.route('/orchestrator/api/v1.0/circuit/<int:circuit_id>', methods = ['GET'])
# @auth.login_required
def get_circuit(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    return jsonify( { 'circuit': make_circuit(circuit[0]) } )
 
@app.route('/orchestrator/api/v1.0/circuits', methods = ['POST'])
# @auth.login_required
def create_circuit():
    if not request.json or not 'service_type' in request.json:
        abort(400)
    circuit = {
        'id': circuits[-1]['id'] + 1,
        'service_type': request.json['service_type'],
        'start_ip_address': request.json.get('start_ip_address', ""),
        'end_ip_address': request.json.get('end_ip_address', ""),
        'active': False
    }
    circuits.append(circuit)
    '''
    # Call OVSDB json-rpc  to configure TEP
  
    rpc_ovsdb_create_tep()	
    Compute node:
    start_ip = 192.168.1.182
    end_ip = 192.168.1.183
    ovs-vsctl add-port br0 vxlan -- set Interface vxlan type=vxlan options:key=10 options:local_ip=192.168.1.183 options:remote_ip=192.168.1.182  ofport_request=10
    ovs-vsctl add-port br0 vxlan -- set Interface vxlan type=vxlan options:key=10 options:local_ip=192.168.1.182 options:remote_ip=192.168.1.183 ofport_request=10
    json-rpc client call
    rpc_faultmonitor_start(id, start_ip_address, end_ip_address);

    '''
    return jsonify( { 'circuit': make_circuits(circuits) } ), 201
 
@app.route('/orchestrator/api/v1.0/circuits/<int:circuit_id>', methods = ['PUT'])
# @auth.login_required
def update_circuits(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'service_type' in request.json and type(request.json['service_type']) != unicode:
        abort(400)
    if 'start_ip_address' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'active' in request.json and type(request.json['active']) is not bool:
        abort(400)
    circuit[0]['service_type'] = request.json.get('service_type', circuit[0]['service_type'])
    circuit[0]['start_ip_address'] = request.json.get('start_ip_address', circuit[0]['start_ip_address'])
    circuit[0]['end_ip_address'] = request.json.get('end_ip_address', circuit[0]['end_ip_address'])
    circuit[0]['classifier'] = request.json.get('classifier', circuit[0]['classifier'])
    circuit[0]['active'] = request.json.get('active', circuit[0]['active'])
    return jsonify( { 'circuit': make_circuit(circuit[0]) } )
    
@app.route('/orchestrator/api/v1.0/circuits/<int:circuit_id>', methods = ['DELETE'])
# @auth.login_required
def delete_circuits(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    circuits.remove(circuit[0])
    return jsonify( { 'result': True } )

@app.route('/compute/api/v1.0/faultmonitor/<int:circuit_id>', methods = ['POST'])
# @auth.login_required
def compute_faultmonitor_start(circuit_id, start_ip, end_ip):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    # ping_start (end_ip);
    return jsonify( { 'result': True } )
    
@app.route('/compute/api/v1.0/performancemetrics/<int:circuit_id>', methods = ['GET'])
# @auth.login_required
def compute_performance_metrics_get(circuit_id):
    circuit = filter(lambda t: t['id'] == circuit_id, circuits)
    if len(circuit) == 0:
        abort(404)
    return jsonify( { 'circuit': make_circuit_metrics(circuit_id, latency, throughput) } ), 201
    
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
        'active': True
    }
    return jsonify( { 'circuit': make_circuits(circuits) } ), 201
'''

    
if __name__ == '__main__':
    app.run(debug = True)

