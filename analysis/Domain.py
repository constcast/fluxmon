from DNSRecord import DNSRecord

class Domain:
	def __init__(self, name):
		self.name = name
		self.ips = []
		self.asns = []
		self.minTTL = 0
		self.maxTTL = 0
		

	def addRecord(self, DNSRecord):
		
		pass
