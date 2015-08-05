import logging

logger = logging.getLogger("qa.{}".format(__name__))


def start_backup(backup_client, group_id, cluster_id):
	config = {
		"groupId": str(group_id),
		"clusterId": str(cluster_id),
		"statusName": "STARTED",
		"syncSource": "PRIMARY"
	}
	return backup_client.patch_config(group_id, cluster_id, config)


def is_backup_working(backup_client, group_id, cluster_id):
	status = backup_client.get_config(group_id, cluster_id)
	status_name = status.get("statusName")
	if status_name == "STARTED":
		return False
	return True

def block_on_backup_finishing(backup_client, group_id, cluster_id):
	while is_backup_working(backup_client, group_id, cluster_id):
		time.sleep(10)
		logger.debug("polling backup")
