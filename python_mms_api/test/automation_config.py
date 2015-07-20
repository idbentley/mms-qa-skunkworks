
def test_basic_parse():
	json = """{
	    "options": {
		"downloadBase": "/var/lib/mongodb-mms-automation"
	    },
	    "mongoDbVersions": [
		{ "name": "3.0.4" }
	    ],
	    "monitoringVersions": [
		{
		    "hostname": "<hostname>",
		    "logPath": "/var/log/mongodb-mms-automation/monitoring-agent.log",
		    "logRotate": {
			"sizeThresholdMB": 1000,
			"timeThresholdHrs": 24
		    }
		}
	    ]
	    "backupVersions": [],
	    "processes": [
		{
		    "version": "3.0.4",
		    "name": "<process_name_1>",
		    "hostname": "<hostname>",
		    "logRotate": {
			"sizeThresholdMB": 1000,
			"timeThresholdHrs": 24
		    },
		    "authSchemaVersion": 1,
		    "processType": "mongod",
		    "args2_4": {
			"port": 27017,
			"replSet": "rs1",
			"dbpath": "/data/",
			"logpath": "/data/mongodb.log"
		    }
		},
	    ]
	    "replicaSets": [
		{
		    "_id": "rs1",
		    "members": [
			{
			    "_id": 0,
			    "host": "<process_name_1>",
			    "priority": 1,
			    "votes": 1,
			    "slaveDelay": 0,
			    "hidden": false,
			    "arbiterOnly": false
			},
		    ]
		},
	    ]
	    "sharding": []
	}"""
	AutomationConfig.parse_json(json)
