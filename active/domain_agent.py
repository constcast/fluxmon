from twisted.internet import reactor
from twisted.names import client

import os, sys, time, socket

class Domain:
	def __init__(self, logdir, domainname, resolver):
		self.logdir = logdir
		self.name = domainname
		self.resolver = resolver		
		self.lookupAddress()

	def lookupAddress(self):
		d = self.resolver.lookupAddress(self.name)
		sucess = lambda (answers, auth, add): self.printAnswer((answers, auth, add))
		failure = lambda (args): self.printFailure(args)
		d.addCallbacks(sucess, failure)

	def printAnswer(self, (answers, auth, add)):
		cur_time = time.time()
		if not len(answers):
			print 'No Answers'
			# call again in an hour
			reactor.callLater(3600, self.lookupAddress)
			return
		self.ttl = 360000
		f = open(self.logdir + "/" + self.name, 'a')
		for x in answers:

			if x.type == 1:
				# we have an A record
				a =  socket.inet_ntoa(x.payload.address)
				f.write(("A %s %d %s %f\n") % (self.name, x.payload.ttl, a, cur_time))
				
			if x.payload.ttl < self.ttl:
				self.ttl = x.payload.ttl
		f.close()

		print "Got resolution for ", self.name, ". Rescheduling in ", self.ttl, " seconds ..."
		reactor.callLater(self.ttl + 1, self.lookupAddress)

	def printFailure(self, arg):
		print "Error: could not resolve \"", self.name, "\". Trying again in two minutes ..."
		# lookup in an hour again
		reactor.callLater(120, self.lookupAddress)

class DomainAgent:
	def __init__(self, storage_dir, domain_db, update_file):
		self.domain_db = domain_db
		self.storage_dir = storage_dir
		self.resolver = client.Resolver('/etc/resolv.conf')
		self.domain_list = dict()
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
		self.domain_list[domain] = Domain(self.storage_dir, domain, self.resolver);
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
