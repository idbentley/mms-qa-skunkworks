import logging

logger = logging.getLogger("qa.{}".format(__name__))

def get_cluster_id_for_rs(cluster_client, group_id, rs_id):
	cluster_id = None
	while True:
		cluster_id = cluster_client.get_cluster_for_replica_set(group_id, rs_id)
		if cluster_id:
			return cluster_id
