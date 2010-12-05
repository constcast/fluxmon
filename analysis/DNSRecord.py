
class DNSRecord:
	def __init__(self, line, tree):
		# Expected Format: "Record Type" "Domain" "TTL" "IP" "timestamp"
		self.tree = tree
		(self.record, self.name, self.ttl, self.ip, self.timestamp) = line.split()


