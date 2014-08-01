#!/usr/bin/env python

__author__ = 'xsited'
import httplib
import json
import base64
import string
from urlparse import urlparse

toggle = 1
toggle_pcmm = 1
circuit_id = 1
# consider refectoring with request http://docs.python-requests.org/en/latest/index.html

class Error:
    # indicates an HTTP error
    def __init__(self, url, errcode, errmsg, headers):
        self.url = url
        self.errcode = errcode
        self.errmsg = errmsg
        self.headers = headers
    def __repr__(self):
        return (
            "<Error for %s: %s %s>" %
            (self.url, self.errcode, self.errmsg)
            )


class RestfulAPI(object):
    def __init__(self, server):
        self.server = server
        self.path = '/wm/staticflowentrypusher/json'
        self.auth = ''
        self.port = 8080

    def get_server(self):
        return self.server

    def set_server(self, server):
        self.server = server


    def set_path(self, path):
	#print path
        self.path = path

#    def set_path(self, path, port):
#        self.path = path
#        self.port = port

    def set_port(self, port):
	#print port
        self.port = port

    def use_creds(self):
    	u = self.auth is not None and len(self.auth) > 0
#    	p = self.password is not None and len(self.password) > 0
        return u

    def credentials(self, username, password):
        self.auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    def get(self, data=''):
        ret = self.rest_call({}, 'GET')
        #return json.loads(ret[2])
        return ret

    def set(self, data):
        #ret = self.rest_call(data, 'PUT')
        ret = self.rest_call2(data, 'PUT')
	print ret[0], ret[1]
        # return ret[0] == 200
        return ret

    def post(self, data):
        ret = self.rest_call(data, 'POST')
        #ret = self.rest_call2(data, 'POST')
	print ret[0], ret[1]
	return ret

    def put(self, data):
        ret = self.rest_call(data, 'PUT')
        return ret
        #return ret[0] == 200


    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        #return ret[0] == 200
        return ret

    def show(self, data):
	print ""
	print json.dumps(data, indent=4, sort_keys=True)
#       print 'DATA:', repr(data)
#
#	print ""
#       data_string = json.dumps(data)
#       print 'JSON:', data_string
#
#	print ""
#       data_string = json.dumps(data)
#       print 'ENCODED:', data_string
#
#	print ""
#       decoded = json.loads(data_string)
#       print 'DECODED:', decoded


    def rest_call2(self, data, action):

        #conn = httplib.HTTPConnection(self.server, self.port)
        conn = httplib.HTTP(self.server, self.port)
        conn.putrequest(action, self.path)
	conn.putheader("Host", self.server+':%s'%self.port)
 	conn.putheader("User-Agent", "Python HTTP Auth")
        conn.putheader('Content-type', 'application/json')
        body = json.dumps(data)
	#conn.putheader("Content-length", "%d" % len(data))
	conn.putheader("Content-length", "%d" % len(body))
        if self.use_creds():
        #    print "using creds"
            conn.putheader("Authorization", "Basic %s" % self.auth)
        conn.endheaders()
	
        conn.send(body)
	errcode, errmsg, headers = conn.getreply()
	ret = (errcode, errmsg, headers)

        #if errcode != 201:
        #   raise Error(self.path, errcode, errmsg, headers)

        # get response
        #response = conn.getresponse()
	#headers = response.read()
        #ret = (response.status, response.reason, headers)
        #if response.status != 200:
        #    raise Error(self.path, response.status, response.reason, headers)
	return ret


    def rest_call(self, data, action):
        body = json.dumps(data)
	if self.use_creds():
	#    print "using creds"
            headers = {
                'Content-type': 'application/json',
                'Accept': 'application/json',
		'Content-length': "%d" % len(body),
	        'Authorization': "Basic %s" % self.auth,
                }
        else:
            headers = {
                'Content-type': 'application/json',
                'Accept': 'application/json',
		'Content-length': "%d" % len(body),
                }
		
	print self.server+':',self.port, self.path
        conn = httplib.HTTPConnection(self.server, self.port)
        conn.request(action, self.path, body, headers)
        response = conn.getresponse()
	data = response.read()
        ret = (response.status, response.reason, data)
        #print "status %d %s" % (response.status,response.reason)
        conn.close()
        return ret


class Menu(object):
    def __init__(self):
        pass

    def print_menu(self):
        print (30 * '-')
        print ("   MENU      ")
        print (30 * '-')
        print ("a. Openflow           ")
        print ("b. Orchestration      ")
        print ("c. Main               ")
        print ("q. Quit               ")

    def print_ormenu(self):
        print (30 * '-')
        print ("   ORCHESTRATION      ")
        print (30 * '-')
        print ("17. Hello             ")
        print ("18. Circuit Get All   ")
        print ("19. Circuit Get One   ")
        print ("20. Circuit Add       ")
        print ("21. Circuit Update    ")
        print ("22. Circuit Delete    ")
        print ("23. Circuit Remove All")
        print ("24. Fault Monitor Service ")
        print ("25. Compute Performance Metrics")
        print ("26. Compute Create    ")
	print ("27. Compute Delete    ")
        print ("28. Compute Ping      ")
        print ("29. Orchestration Report Status")
        print ("30. Orchestration Report Metrics")
        print ("31. Orchestration Performance Metrics")
        print ("c. Main               ")
        print ("q. Quit               ")
#        print (30 * '-')


    def print_ofmenu(self):
        print (30 * '-')
        print ("   OPENFLOW               ")
        print (30 * '-')
        print ("1.  Add Flow 1        ")
        print ("2.  Add Flow 2        ")
        print ("3.  Add Several Flows ")
        print ("4.  Remove Flow 1     ")
        print ("5.  Remove Flow 2     ")
        print ("6.  Remove All Flows  ")
        print ("7.  Toggle Flow       ")
        print ("8.  List Flow Stats   ")
        print ("9.  List Topology     ")
        print ("10. List Flows        ")
        print ("11. List Ports        ")
        print ("12. Add PCMM Flow 1   ")
        print ("13. Remove PCMM Flow 1")
        print ("14. Add PCMM Flow 2   ")
        print ("15. Remove PCMM Flow 2")
        print ("16. Toggle PCCM Flows")
        print ("c. Main               ")
        print ("q. Quit               ")
#        print (30 * '-')


    def no_such_action(self):
        print "Invalid option!"

    def run(self):
	self.print_menu()
        actions = {
	"a": self.print_ofmenu,
	"b": self.print_ormenu,
	"c": self.print_menu,
	"1": flow_add_1, 
	"2": flow_add_2, 
	"3": flow_add_several, 
	"4": flow_remove_1,
	"5": flow_remove_2,
	"6": flow_remove_all,
	"7": flow_toggle,
	"8": flow_list_stats,
	"9": topology_list,
	"10":flow_list,
	"11":port_list,
	"12":flow_add_pc_1,
	"13":flow_remove_pc_1,
	"14":flow_add_pc_2,
	"15":flow_remove_pc_2,
	"16":flow_toggle_pcmm,
	"17":hello,
	"18":orchestration_circuit_get_all,
	"19":orchestration_circuit_get_one,
	"20":orchestration_circuit_add,
	"21":orchestration_circuit_update,
	"22":orchestration_circuit_delete,
	"23":orchestration_circuit_remove_all,
	"24":compute_faultdetection_service,
        "25":compute_performance_metrics_get,
	"26":compute_create_circuit,
	"27":compute_delete_circuit,
	"28":compute_ping,
	"29":orchestration_report_status,
	"30":orchestration_report_metrics,
	"31":orchestration_performance_metrics,
	"32":hello_cubies,
	"33":compute_create_circuit_cubies,
	"q": exit_app,
        }

        while True:
            #self.print_ormenu()
            selection = raw_input("Enter selection: ")
            if "quit" == selection:
                return
            toDo = actions.get(selection, self.no_such_action)
            toDo()




class ODL(object):
    def __init__(self):
        pass

    def topology(self):
        ws.set_path('/controller/nb/v2/topology/default')
	ws.set_port(8080)	
        content = ws.get()
        j=json.loads(content[2])
        ws.show(j)

    def statistics_ports(self):
        ws.set_path('/controller/nb/v2/statistics/default/port')
	ws.set_port(8080)	
        content = ws.get()
        allPortStats = json.loads(content[2])
	# ws.show(allPortStats)
        portStats = allPortStats['portStatistics']
	# XXX - Array traversal missing last element?
        for po in portStats:
	    print "\nSwitch ID : " + po['node']['id'] +  " Type: " +  po['node']['type']
            for so in po['portStatistic']:
	       # ws.show( so )
	       nc = so['nodeConnector']
               print "\nPort : " + nc['id'] + " Type: " +  nc['type'] 
	       print "Connector Node : " + nc['node']['id'] +  " Type : " +  nc['node']['type']
               print "    Received Bytes  :        ", so['receiveBytes']
               print "    Received Packets:        ", so['receivePackets']
               print "    Received Drops:          ", so['receiveDrops']
               print "    Received Errors:         ", so['receiveErrors']
               print "    Received Frame Errors:   ", so['receiveFrameError']
               print "    Received Over Run Error: ", so['receiveOverRunError']
               print "    Received CRC Errors:     ", so['receiveCrcError']
               print "    Transmitted Packets:     ", so['transmitBytes']
               print "    Transmitted Errors:      ", so['transmitErrors']
               print "    Transmitted Drops:       ", so['transmitDrops']
               print "    Collision Count:         ", so['collisionCount']


    # adopted from fredhsu @ http://fredhsu.wordpress.com/2013/04/25/getting-started-with-opendaylight-and-python/
    def statistics_flows(self):
        ws.set_path('/controller/nb/v2/statistics/default/flow')
	ws.set_port(8080)	
        content = ws.get()
        allFlowStats = json.loads(content[2])

        flowStats = allFlowStats['flowStatistics']
	# These JSON dumps were handy when trying to parse the responses 
        #print json.dumps(flowStats[0]['flowStat'][1], indent = 2)
	#print json.dumps(flowStats[4], indent = 2)
        for fs in flowStats:
            print "\nSwitch ID : " + fs['node']['id']
	    print '{0:8} {1:8} {2:5} {3:15}'.format('Count', 'Action', 'Port', 'DestIP')
	    if not 'flowStatistic' in fs.values(): 
		print '              none'
		continue
	    for aFlow in fs['flowStatistic']:
		#print "*", aFlow, "*", " ", len(aFlow), " ", not aFlow
	        count = aFlow['packetCount']
	        actions = aFlow['flow']['actions'] 
	        actionType = ''
	        actionPort = ''
	        #print actions
	        if(type(actions) == type(list())):
		    actionType = actions[1]['type']
		    actionPort = actions[1]['port']['id']
		else:
	    	    actionType = actions['type']
		    actionPort = actions['port']['id']
		dst = aFlow['flow']['match']['matchField'][0]['value']
		print '{0:8} {1:8} {2:5} {3:15}'.format(count, actionType, actionPort, dst)

    def flowprogrammer_list(self):
        ws.set_path('/controller/nb/v2/flowprogrammer/default')
	ws.set_port(8080)	
        content = ws.get()
        j=json.loads(content[2])
        ws.show(j)
        #ws.show(content[2])
	return(j)


    def flowprogrammer_add(self, flow):
        # http://localhost:8080/controller/nb/v2/flowprogrammer/default/node/OF/00:00:00:00:00:00:00:01/staticFlow/flow1
        ws.set_path('/controller/nb/v2/flowprogrammer/default/node/' + flow['node']['type'] + '/' + flow['node']['id'] + '/staticFlow/' + flow['name'] )
	ws.set_port(8080)	
        ws.show(flow)
        content = ws.set(flow)
        #print content
	flowadd_response_codes = {
	201:"Flow Config processed successfully",
	400:"Failed to create Static Flow entry due to invalid flow configuration",
	401:"User not authorized to perform this operation",
	404:"The Container Name or nodeId is not found",
	406:"Cannot operate on Default Container when other Containers are active",
	409:"Failed to create Static Flow entry due to Conflicting Name or configuration",
	500:"Failed to create Static Flow entry. Failure Reason included in HTTP Error response",
	503:"One or more of Controller services are unavailable",
	} 
	msg=flowadd_response_codes.get(content[0])
	print content[0], content[1], msg

    def flowprogrammer_remove(self, flow):
        ws.set_path('/controller/nb/v2/flowprogrammer/default/node/' + flow['node']['type'] + '/' + flow['node']['id'] + '/staticFlow/' + flow['name'] )
	ws.set_port(8080)	
        content = ws.remove("", flow)

	flowdelete_reponse_codes = {
	204:"Flow Config deleted successfully",
	401:"User not authorized to perform this operation",
	404:"The Container Name or Node-id or Flow Name passed is not found",
	406:"Failed to delete Flow config due to invalid operation. Failure details included in HTTP Error response",
	500:"Failed to delete Flow config. Failure Reason included in HTTP Error response",
	503:"One or more of Controller service is unavailable",
	}
	msg=flowdelete_reponse_codes.get(content[0])
	print content[0], content[1], msg

    def flowprogrammer_remove_all(self):
	allFlowConfigs = self.flowprogrammer_list()
        flowConfigs = allFlowConfigs['flowConfig']
	# These JSON dumps were handy when trying to parse the responses 
        #print json.dumps(flowStats[0]['flowStat'][1], indent = 2)
	#print json.dumps(flowStats[4], indent = 2)
        for fl in flowConfigs:
	    print "Removing ", fl['name']
    	    self.flowprogrammer_remove(fl)
		

class OClient(object):

    def __init__(self):
        pass

    # curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/hello
    def o_hello(self):
	ws.set_path('/orchestrator/api/v1.0/hello')	
	ws.set_port(5555)	
	content = ws.get()
        j=json.loads(content[2])
        ws.show(j)


    # curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/circuits
    def o_circuit_get_all(self):
	ws.set_path('/orchestrator/api/v1.0/circuits')
	ws.set_port(5555)	
	content = ws.get()
        j=json.loads(content[2])
        ws.show(j)
 
    # curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/circuits/2
    def o_circuit_get(self, circuit_id):
	ws.set_path('/orchestrator/api/v1.0/circuits/' + circuit_id)
	ws.set_port(5555)	
	content = ws.get()
        j=json.loads(content[2])
        ws.show(j)

    # curl -i -u user:password -H "Content-Type: application/json" -X POST -d '
    #	  {  
    #    "service_type": "epl", 
    #	  "start_ip_address": "192.168.1.3", 
    #	  "end_ip_address": "192.168.1.4", 
    #	  "classifier": "red", 
    #    "self": "http://localhost:8888/service_id/1" 
    #    } 
    #    http://localhost:5555/orchestrator/api/v1.0/circuits
    def o_circuit_create(self, circuit):
        ws.set_path('/orchestrator/api/v1.0/circuits')
	ws.set_port(5555)	
        ws.show(circuit)
	content = ws.post(circuit)
        j=json.loads(content[2])
        ws.show(j)

    # curl -i -u user:password -H "Content-Type: application/json" -X PUT -d '
    #	{ "id": 1, 
    #	  "service_type": "epl", 
    #	  "start_ip_address": "192.168.1.3", 
    #	  "end_ip_address": "192.168.1.4", 
    #	  "classifier": "blue", 
    #	  "self": "http://localhost:8888/service_id/1", 
    #	  "active": true 
    #	}
    #    ' http://localhost:5555/orchestrator/api/v1.0/circuits/1
    def o_circuit_update(self, circuit_id, circuit):
        ws.set_path('/orchestrator/api/v1.0/circuits/' + circuit_id)
	ws.set_port(5555)	
	content = ws.put(circuit)
        j=json.loads(content[2])
        ws.show(j)

    def o_circuit_delete(self, circuit_id):
        ws.set_path('/orchestrator/api/v1.0/circuits/' + circuit_id)
	ws.set_port(5555)	
	content = ws.remove("",circuit1)
        j=json.loads(content[2])
        ws.show(j)


    # curl -i  -H "Content-Type: application/json" -X PUT -d '{"start_ip_address":"2.2.2.2","self":"http://local/1","end_ip_address":"1.1.1.1","service_type":"vepl","classifier":"11","active":true}' http://localhost:5555/compute/api/v1.0/circuits/1
    def c_circuit_create_on_server(self, circuit, server):
        ws.set_path('/compute/api/v1.0/circuits')
	ws.set_port(5555)	
    	temp_server=ws.get_server()
    	print "Temp Server = ", temp_server
    	ws.set_server( server )
    	print "Server = ", ws.get_server()
        ws.show(circuit)
	content = ws.post(circuit)
        j=json.loads(content[2])
        ws.show(j)
    	ws.set_server(temp_server)

    def c_circuit_delete_on_server(self, circuit_id, server):
        ws.set_path('/compute/api/v1.0/circuits/%d' % circuit_id)
	ws.set_port(5555)	
    	temp_server=ws.get_server()
    	ws.set_server( server )
	content = ws.remove("",circuit1)
        j=json.loads(content[2])
        ws.show(j)
    	ws.set_server(temp_server)

    def c_hello(self, server):
	ws.set_path('/orchestrator/api/v1.0/hello')	
	ws.set_port(5555)	
    	temp_server=ws.get_server()
    	ws.set_server( server )
	content = ws.get()
        j=json.loads(content[2])
        ws.show(j)
    	ws.set_server(temp_server)



    # curl -i  -H "Content-Type: application/json" -X PUT -d '{"active":true}' http://localhost:5555/orchestrator/api/v1.0/circuits/1
    # curl -i  -H "Content-Type: application/json" -X PUT -d '{"active":true}' http://localhost:5555/orchestrator/api/v1.0/circuits/1

    def c_faultdetection_service(self, circuit_id, on):
        ws.set_path('/compute/api/v1.0/faultmonitor/%d' % circuit_id)
	ws.set_port(5555)	
        content = ws.get()
        j=json.loads(content[2])
        ws.show(j)

    def o_report_status_self(self,circuit_id, uri, status):
    	temp_server=ws.get_server()
	#XXX - validate
        o = urlparse(uri)
        tmp = o.netloc.split(":",2)
	print tmp
	print o.path
	print o.netloc
        ws.set_server(tmp[0])
        ws.set_port(tmp[1])
        ws.set_path(o.path)
        content = ws.put(status)
        j=json.loads(content[2])
        ws.show(j)
    	ws.set_server(temp_server)

    def o_report_status(self,circuit_id, status, server):
        ws.set_path('/orchestrator/api/v1.0/reportstatus/'+circuit_id)
	ws.set_port(5555)	
    	temp_server=ws.get_server()
    	ws.set_server( server )
        content = ws.put(status)
        j=json.loads(content[2])
        ws.show(j)
    	ws.set_server(temp_server)

    def o_report_metrics(self,circuit_id, metrics):
        ws.set_path('/orchestrator/api/v1.0/reportmetrics/'+circuit_id)
	ws.set_port(5555)	
        content = ws.put(metrics)
        j=json.loads(content[2])
        ws.show(j)

    def o_performance_metrics(self,circuit_id):
        ws.set_path('/orchestrator/api/v1.0/performancemetrics/'+circuit_id)
	ws.set_port(5555)	
        content = ws.get()
        j=json.loads(content[2])
        ws.show(j)


    def c_performance_metrics_get(self,circuit_id, server):
        ws.set_path('/compute/api/v1.0/performancemetrics/%d' % circuit_id)
	ws.set_port(5555)	
    	temp_server=ws.get_server()
    	ws.set_server( server )
        content = ws.get()
        j=json.loads(content[2])
        ws.show(j)
    	ws.set_server(temp_server)




# XXX - do not use underscores and dashes in flow names.
# XXX - ingress ports that possibly don't exist ? throw configuration errors
circuit1 = {  
          "service_type": "epl", 
	  "start_ip_address": "10.0.0.133", 
	  "end_ip_address": "10.0.0.134", 
     	  "classifier": "red", 
          "self": "http://10.36.0.192:9000/vcpe-service/53dbfa230607df6d45ab66e8",
	  "active": False 
}

circuit2 = { 
	  "service_type": "epl", 
	  "start_ip_address": "192.168.1.3", 
	  "end_ip_address": "192.168.1.4", 
	  "classifier": "blue", 
          "self": "http://10.36.0.192:9000/vcpe-service/53dbfa230607df6d45ab66e8",
	  "active": True 
}


flow1 = {
        "actions": [
            "OUTPUT=2"
        ],         
        "installInHw":"false",
        "name":"flow1",
        "node":
        {
            "id":"00:00:00:00:00:00:00:02",
            "type":"OF"
        }, 
        "priority":"500",
        "etherType":"0x800",
        "nwSrc":"10.0.0.7",
        "tpSrc":"8081",
        "nwDst":"10.0.0.3", 
}

flow2 = {
        "actions": [
            "OUTPUT=2"
        ],         
        "installInHw":"false",
        "name":"flow2",
        "node":
	{
	    "id":"00:00:00:00:00:00:00:01",
	    "type":"OF"
        },
        "priority":"500",
        "etherType":"0x800",
        "nwSrc":"10.0.0.1",
        "tpSrc":"1369",
        "nwDst":"10.0.0.3", 
}


flow3 = {
     "actions": [
        "OUTPUT=3"
     ], 
     "etherType": "0x800", 
     "installInHw": "true", 
     "name": "flow2", 
     "node": {
           "id": "00:00:00:00:00:00:00:01", 
           "type": "OF"
     }, 
     "nwDst": "10.0.0.2", 
     "nwSrc": "10.0.0.1", 
     "priority": "500", 
     "protocol": "6"
} 


flow5={
     "actions": [
          "OUTPUT=2"
     ], 
     "etherType": "0x800", 
     "installInHw": "false", 
     "name": "flow5", 
     "node": {
         "id": "00:00:00:00:00:00:00:01", 
          "type": "OF"
      }, 
     "nwSrc": "10.0.0.10", 
     "priority": "500"
}

flow4={
   "actions": [
       "OUTPUT=2"
   ], 
   "etherType": "0x800", 
   "installInHw": "true", 
   "name": "flow4", 
   "node": {
           "id": "00:00:00:00:00:00:00:01", 
           "type": "OF"
    }, 
    "nwSrc": "10.0.0.1", 
    "priority": "500", 
    "vlanId": "1", 
    "vlanPriority": "1"
}

''' Demo Kit  Layout

flow_pcmm_1 = {
     "actions": [
        "FLOOD"
     ], 
     "etherType": "0x800", 
     "installInHw": "true", 
     "name": "flowpcmmHighBW", 
     "node": {
           "id": "51966", 
           "type": "PC"
     }, 
     "tpDst":"8081",
     "nwDst": "10.32.4.208", 
     "nwSrc": "10.32.154.2", 
     "priority": "100", 
} 

flow_pcmm_2 = {
     "actions": [
        "FLOOD"
     ], 
     "etherType": "0x800", 
     "installInHw": "true", 
     "name": "flowpcmmLowBW", 
     "node": {
           "id": "51966", 
           "type": "PC"
     }, 
     "tpDst":"8081",
     "nwDst": "10.32.4.208", 
     "nwSrc": "10.32.154.2", 
     "priority": "64", 
} 
'''


''' LAB Workbench Layout 
'''

flow_pcmm_1 = {
     "actions": [
        "FLOOD"
     ], 
     "etherType": "0x800", 
     "installInHw": "true", 
     "name": "flowpcmmHighBW", 
     "node": {
           "id": "51966", 
           "type": "PC"
     }, 
     "tpDst":"8081",
     "nwDst": "10.200.90.10",
     "nwSrc": "10.50.201.151",
     "priority": "100", 
} 

flow_pcmm_2 = {
     "actions": [
        "FLOOD"
     ], 
     "etherType": "0x800", 
     "installInHw": "true", 
     "name": "flowpcmmLowBW", 
     "node": {
           "id": "51966", 
           "type": "PC"
     }, 
     "tpDst":"8081",
     "nwDst": "10.200.90.10",
     "nwSrc": "10.50.201.151",
     "priority": "64", 
} 


def flow_add_pc_1():
    print "Test PCMM Flow 1     "
    odl.flowprogrammer_add(flow_pcmm_1)

def flow_remove_pc_1():
    print "Remove PCMM Flow 1  "
    odl.flowprogrammer_remove(flow_pcmm_1)


def flow_add_pc_2():
    print "Test PCMM Flow 2     "
    odl.flowprogrammer_add(flow_pcmm_2)

def flow_remove_pc_2():
    print "Remove PCMM Flow 2  "
    odl.flowprogrammer_remove(flow_pcmm_2)

def flow_toggle_pcmm():
    print "Toggle Flow    "
    global toggle_pcmm
    toggle_pcmm = 3 - toggle_pcmm
    if toggle_pcmm == 1:
	flow_remove_pc_2()
	flow_add_pc_1()
    else:
	flow_remove_pc_1()
	flow_add_pc_2()

def flow_add_1():
    print "Add Flow 1     "
    odl.flowprogrammer_add(flow1)


def flow_add_2():
    print "Add Flow 2     "
    odl.flowprogrammer_add(flow2)

def flow_add_several():
    print "Add Flow Several     "
    odl.flowprogrammer_add(flow1)
    odl.flowprogrammer_add(flow2)
    odl.flowprogrammer_add(flow3)
    odl.flowprogrammer_add(flow4)
    odl.flowprogrammer_add(flow5)


def flow_toggle():
    print "Toggle Flow    "
    global toggle
    toggle = 3 - toggle
    if toggle == 1:
	flow_remove_2()
	flow_add_1()
    else:
	flow_remove_1()
	flow_add_2()


def flow_remove_1():
    print "Remove Flow 1  "
    odl.flowprogrammer_remove(flow1)

def flow_remove_2():
    print "Remove Flow 2  "
    odl.flowprogrammer_remove(flow2)

def flow_remove_all():
    print "Remove All Flows "
    odl.flowprogrammer_remove_all()

def flow_list_stats():
    print "List Flow Stats"
    odl.statistics_flows()

def topology_list():
    print "List Topology  "
    odl.topology()

def flow_list():
    print "List Flows  "
    odl.flowprogrammer_list()

def port_list():
    print "List Ports Stats  "
    odl.statistics_ports()


def exit_app():
    print "Quit           "
    exit(0)

def orchestration_circuit_get_all():
    print "Orchestration Get All Circuits"
    oc.o_circuit_get_all()

def orchestration_circuit_get_one():
    print "Orchestration Get One"
    circuit_id = raw_input("Enter circuit id: ")
    if "quit" == circuit_id:
         return
    oc.o_circuit_get(circuit_id)
    


def orchestration_circuit_add():
    print "Orchestration Circuit Add"
    global circuit1
    circuit_id1=oc.o_circuit_create(circuit1)

def orchestration_circuit_update():
    print "Orchestration Circuit Update"
    global circuit1
    global circuit2
    global circuit_id1
    circuit_id = raw_input("Enter circuit id: ")
    if "quit" == circuit_id:
         return
    oc.o_circuit_update(circuit_id, circuit2)

def orchestration_circuit_delete():
    print "Orchestration Circuit Delete"
    circuit_id = raw_input("Enter circuit id: ")
    if "quit" == circuit_id:
         return
    oc.o_circuit_delete(circuit_id)

def orchestration_circuit_remove_all():
    print "Orchestration Circuit Remove All"

def compute_faultdetection_service():
    print "Compute Fault Service"
    circuit_id = raw_input("Enter circuit id: ")
    if "quit" == circuit_id:
         return
    onoff = raw_input("Enter on = 1 or off = 0: ")
    if "quit" == onoff:
         return
    oc.c_faultdetection_service(circuit_id,onoff)

def orchestration_performance_metrics():
    print "Orchestration Performance  Metrics"
    circuit_id = raw_input("Enter circuit id: ")
    if "quit" == circuit_id:
         return
    oc.o_performance_metrics(circuit_id)

metrics1={
    "metrics": {
        "id": 2, 
        "latency": "0.412927117459", 
        "latency_UnitMeasurement": "ms", 
        "throughput": 100, 
        "throughput_UnitMeasurement": "Mbps"
    }, 
    "status": "ok"
}

def orchestration_report_metrics():
    print "Orchestration Report  Metrics"
    circuit_id = raw_input("Enter circuit id: ")
    if "quit" == circuit_id:
         return
    oc.o_report_metrics(circuit_id, metrics1)

def orchestration_report_status():
    print "Orchestration Report  Status"
    circuit_id = raw_input("Enter circuit id: ")
    if "quit" == circuit_id:
         return
    onoff = raw_input("Enter on = 1 or off = 0: ")
    if "quit" == onoff:
         return
    if onoff == "1":
        print "True"
	status = { 
		"status" : "running"
	}
    else:
        print "False"
	status = { 
		"status" : "suspended"
	}

    oc.o_report_status(circuit_id, status)

def compute_performance_metrics_get():
    print "Compute Performance  Metrics"
    circuit_id = raw_input("Enter circuit id: ")
    if "quit" == circuit_id:
         return
    oc.c_performance_metrics_get(int(circuit_id), circuit3['start_ip_address'])

circuit3 = { 
	  "service_type": "epl", 
	  "start_ip_address": "10.0.0.133", 
	  "end_ip_address": "10.0.0.134", 
	  "classifier": "blue", 
	  "self": "http://localhost:8888/service_id/1", 
	  "active": True 
}
circuit4 = { 
	  "service_type": "epl", 
	  "start_ip_address": "10.0.0.135", 
	  "end_ip_address": "10.0.0.136", 
	  "classifier": "blue", 
	  "self": "http://localhost:8888/service_id/1", 
	  "active": True 
}

def hello_cubies():
    print "Compute Create Circuit"
    oc.c_hello(circuit4['start_ip_address'])
    oc.c_hello(circuit4['end_ip_address'])

def compute_create_circuit_cubies():
    print "Compute Create Circuit Cubie"
    oc.c_circuit_create_on_server(circuit4, circuit4['start_ip_address'])
    oc.c_circuit_create_on_server(circuit4, circuit4['end_ip_address'])

def compute_ping():
    print "Compute Create Circuit"
    oc.c_hello(circuit3['start_ip_address'])
    oc.c_hello(circuit3['end_ip_address'])

def compute_create_circuit():
    print "Compute Create Circuit"
    oc.c_circuit_create_on_server(circuit3, circuit3['start_ip_address'])
    oc.c_circuit_create_on_server(circuit3, circuit3['end_ip_address'])

def compute_delete_circuit():
    print "Compute Delete Circuit"
    circuit_id = raw_input("Enter circuit id: ")
    if "quit" == circuit_id:
         return
    oc.c_circuit_delete_on_server(circuit_id, circuit3['start_ip_address'])
    oc.c_circuit_delete_on_server(circuit_id, circuit3['end_ip_address'])

def hello():
    oc.o_hello()

ws = RestfulAPI('127.0.0.1')

if __name__ == "__main__":
    #ws = RestfulAPI('192.168.56.10')
    ws.credentials('admin', 'admin')
    odl = ODL()
    oc = OClient()
    menu=Menu()
    menu.run()
    exit(0)



