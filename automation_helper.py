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
	return old_config
