from twisted.internet import reactor

import os, sys

import domain

class DomainAgent:
	def __init__(self, domain_db, update_file):
		self.domain_db = domain_db
		self.domain_list = []
		print "Reading already known domains ..."
		self.readKnownDomains()
		self.update_file = update_file

	def readKnownDomains(self):
		try:
			f = open(self.domain_db)
			for line in f:
				self.addNewDomain(line.rstrip('\n'))
			f.close()
		except Exception as inst:
			print "Error reading already known domain list: ", inst.args

	def addNewDomain(self, domain):
		if (domain in self.domain_list):
			print "Cannot add domain \"" + domain + "\" because we are already checking it!"
			return False
		print "Adding domain \"" + domain + "\" to domain repository..."
		self.domain_list.append(domain)
		return True
		
		

	def checkForDomainUpdates(self):
		if (os.path.isfile(self.update_file)):
			print "Found update file! Sucking in new domains ..."
			try: 
				f = open(self.update_file);
				for line in f:
					if self.addNewDomain(line.rstrip('\n')):
						# record Domain in known domain db
						try:
							db = open(self.domain_db, 'a')
							db.write(line)
							db.close()
						except Exception as inst:
							print "Error appending domain to domain db: ", inst.args
					
				f.close()
			except Exception as inst:
				print "Error reading update file: ", inst.args
			os.unlink(self.update_file)
		reactor.callLater(2, self.checkForDomainUpdates)

	def run(self):
		# schedule automatic checks for an update domain file
		reactor.callLater(2, self.checkForDomainUpdates)

		# start event loop
		reactor.run()
