import SubnetTree
import re

class ASNTree:
	def __init__(self, inputFile):
		self.tree = SubnetTree.SubnetTree()
		print "Building Subnet to ASN mapping..."
		try:
			for line in open(inputFile, 'r'):
				(ip, mask, asn, null) = re.split('\s+', line)
				self.tree[ip + '/' + mask] = asn
				
		except Exception as inst:
			print "Could not process ASN file: ", inst.args


	def getASN(self, IP):
		try:
			asn = self.tree[IP]
		except KeyError:
			return 0
		return asn
