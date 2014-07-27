#!/bin/sh

curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/hello

curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/circuits

curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/circuits/1
curl -i -u user:password http://localhost:5555/orchestrator/api/v1.0/circuits/2
curl -i -u user:password  -H "Content-Type: application/json" -X DELETE http://localhost:5555/orchestrator/api/v1.0/circuits/4

curl -i -u user:password -H "Content-Type: application/json" -X POST -d '{ "service_type": "epl", "start_ip_address": "192.168.1.3", "end_ip_address": "192.168.1.4", "classifier": "red", "self": "http://localhost:8888/service_id/1" }' http://localhost:5555/orchestrator/api/v1.0/circuits

curl -i -u user:password -H "Content-Type: application/json" -X POST -d '{ "service_type": "epl", "start_ip_address": "192.168.1.5", "end_ip_address": "192.168.1.6", "classifier": "yellow", "self": "http://localhost:8888/service_id/3" }' http://localhost:5555/orchestrator/api/v1.0/circuits


curl -i -u user:password -H "Content-Type: application/json" -X PUT -d '{ "service_type": "epl", "start_ip_address": "192.168.1.3", "end_ip_address": "192.168.1.4", "classifier": "blue", "self": "http://localhost:8888/service_id/1", "active": true }' http://localhost:5555/orchestrator/api/v1.0/circuits/1

curl -i  -H "Content-Type: application/json" -X PUT -d '{"start_ip_address":"2.2.2.2","self":"http://local/1","end_ip_address":"1.1.1.1","service_type":"vepl","classifier":"11","active":true}' http://localhost:5555/orchestrator/api/v1.0/circuits/1

curl -i  -H "Content-Type: application/json" -X PUT -d '{"active":true}' http://localhost:5555/orchestrator/api/v1.0/circuits/1

curl -i -u user:password http://localhost:5555//orchestrator/api/v1.0/performancemetrics/2

curl -i -u user:password  -H "Content-Type: application/json" -X DELETE http://localhost:5555/orchestrator/api/v1.0/circuits/2

curl -i  -H "Content-Type: application/json" -X PUT -d '{"active":true}' http://localhost:5555/debug
