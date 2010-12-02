from twisted.internet import reactor

import os, sys

import domain

class DomainAgent:
	def __init__(self, domain_list, update_file):
		self.domain_list = domain_list
		self.update_file = update_file

	def addNewDomain(self, domain):
		if (domain in self.domain_list):
			print "Cannot add domain \"" + domain + "\" because we are already checking it!"
			return
		print "Adding domain \"" + domain + "\" to domain repository..."
		self.domain_list.append(domain)
		

	def checkForDomainUpdates(self):
		if (os.path.isfile(self.update_file)):
			print "Found update file! Sucking in new domains ..."
			try: 
				f = open(self.update_file);
				for line in f:
					self.addNewDomain(line.rstrip('\n'))
				f.close()
			except Exception as inst:
				print "Error reading update file: ", inst.args
			#os.unlink(self.update_file)
		reactor.callLater(2, self.checkForDomainUpdates)

	def run(self):
		# schedule automatic checks for an update domain file
		reactor.callLater(2, self.checkForDomainUpdates)

		# start event loop
		reactor.run()
