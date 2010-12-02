from twisted.internet import reactor

import os

class DomainAgent:
	def __init__(self, domain_list, update_file):
		self.domain_list = domain_list
		self.update_file = update_file

	def checkForDomainUpdates(self):
		if (os.path.isfile(self.update_file)):
			print "Found update file! Sucking in new domains ..."
			os.unlink(self.update_file)
		reactor.callLater(2, self.checkForDomainUpdates)

	def run(self):
		# schedule automatic checks for an update domain file
		reactor.callLater(2, self.checkForDomainUpdates)

		# start event loop
		reactor.run()
