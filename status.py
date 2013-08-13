import state

class Status:

	def __init__(self, name):
		self.name = name

	def done(self,state):
		print self.name+' ended' 

	// end conditions

	// cleanup

	def aborted(self):
		print self.name+' aborted'

def status_updater(status,state):
	print 'choosing status'

	if status.done(state):
		next_status = status.next

