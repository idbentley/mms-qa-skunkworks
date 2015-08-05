import time
import logging

logger = logging.getLogger("qa.{}".format(__name__))

def add_new_rs(old_config, rs_id, dbpath, hostname, num_members, run_id):
	new_rs = {
		"_id": rs_id,
		"members": []
	}
	for i in range(num_members):
		new_process = {
			"version": "3.0.4",
			"name": rs_id + "_" + str(i),
			"hostname": hostname,
			"authSchemaVersion": 5,
			"processType": "mongod",
			"args2_6": {
				"port": 27000 + run_id + i,
				"replSet": rs_id,
				"storage": {
					"dbPath": dbpath,
				},
				"systemLog": {
					"destination": "file",
					"path": dbpath + "mongodb.log"
				}
			}
			
		}
		old_config["processes"].append(new_process)

		member = {
			"host": rs_id + "_" + str(i),
			"priority": 1,
			"votes": 1,
			"slaveDelay": 0,
			"hidden": False,
			"arbiterOnly": False
		}
		new_rs["members"].append(member)
	old_config["replicaSets"].append(new_rs)
	return rs_id


def add_new_config_server(old_config, hostname, num_id, run_id):
    name = "config_server_{}_{}".format(run_id, num_id)
    new_process = {
	   "name": name,
        "processType": "mongod",
        "version": "3.0.4",
        "hostname": hostname,
        "logRotate": {
            "sizeThresholdMB": 1000,
            "timeThresholdHrs": 24
        },
        "authSchemaVersion": 5,
        "args2_6": {
            "net": {
                "port": 28000 + run_id + num_id
            },
            "storage": {
                "dbPath": "/data/{}".format(name)
            },
            "systemLog": {
                "path": "/data/{}/mongodb.log".format(name),
                "destination": "file"
            },
            "sharding": {
                "clusterRole": "configsvr"
            },
            "operationProfiling": {}
        }
    }
    old_config["processes"].append(new_process)
    return name

def add_new_mongos(old_config, hostname, run_id):
    name = "mongos_{}".format(run_id)
    new_process = {
        "name": name,
        "processType": "mongos",
        "version": "3.0.4",
        "hostname": hostname,
        "cluster": "cluster_{}".format(run_id),
        "logRotate": {
            "sizeThresholdMB": 1000,
            "timeThresholdHrs": 24
        },
        "authSchemaVersion": 5,
        "args2_6": {
            "net": {
                "port": 29000 + run_id
            },
            "systemLog": {
                "path": "/data/{}/mongodb.log".format(name),
                "destination": "file"
            },
            "operationProfiling": {}
        }
    }
    old_config["processes"].append(new_process)


def add_sharding_config(old_config, cluster_name, rs_ids, config_servers):
    new_shard = {
        "name": cluster_name,
        "configServer": [],
        "shards": [],
        "collections": [],
    }
    for rs_id in rs_ids:
    	new_shard["shards"].append({"_id": rs_id, "rs": rs_id})
    for config_server in config_servers:
    	new_shard["configServer"].append(config_server)
    old_config["sharding"].append(new_shard)


def add_new_cluster(old_config, rs_prefix, hostname, num_shards, num_members_per_shard, run_id):
	# create num_shards replicasets
	rs_ids = []
	for i in range(num_shards):
		rs_ids.append(add_new_rs(old_config, "{}_{}_{}".format(rs_prefix, run_id, i), "/data/rs{}_{}".format(run_id, i), hostname, num_members_per_shard, run_id * i))

	# create 3 config_server processes
	cs_names = []
	for i in range(3):
		cs_names.append(add_new_config_server(old_config, hostname, i, run_id))

	# create mongos process
	add_new_mongos(old_config, hostname, run_id)

	# add sharding config
	add_sharding_config(old_config, "cluster_{}".format(run_id), rs_ids, cs_names)

def add_replica_set_to_group(automation_client, hostname, group_id, entropy):
	old_config = automation_client.get_config(group_id)
	rs_id = "integrity-" + str(entropy)
	dbpath = "/data/" + str(entropy) + "_1/"
	add_new_rs(old_config, rs_id, dbpath, hostname, 1, entropy)
	automation_client.update_config(group_id, old_config)
	return rs_id

def block_on_automation_finishing(automation_client, group_id):
	while automation_client.automation_working(group_id):
		time.sleep(10)
		logger.debug("polling automation")
