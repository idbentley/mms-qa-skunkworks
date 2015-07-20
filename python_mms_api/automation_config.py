
monitoring_versions_schema = {
}
backup_versions_schema = {
}
processes_schema = {
}
replica_sets_schema = {
}
sharding_schema = {
}
json_schema = {
	"options": {
		"downloadBase": "string"
	},
	"mongoDbVersions": {
		"type": "array",
		"required": True,
	},
	"monitoringVersions": monitoring_versions_schema,
	"backupVersions": backup_versions_schema,
	"processes": processes_schema,
	"replicaSets": replica_sets_schema,
	"sharding": sharding_schema
}

class AutomationConfig(object):
	options
	mongodb
	monitoring_versions
	backup_versions
	processes
	replica_sets
	sharding

	@classmethod
	def parse_json(json):
		
	def to_json(self):
		
