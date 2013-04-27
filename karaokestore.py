import uuid
from collections import deque
import json

#in memory store

class KaraokeStore(object):
	
	def __init__(self):
		self.users = dict() #key:user_id, value:User object
		self.performances = dict() #key:performance_id, value:(user_id, path_to_file)
		self.main_queue = deque() #performance_id
		self.current_performance = None #performance_id
	

	def queue_performance(self, user_id, path_to_file):
		performance_id = str(uuid.uuid4())
		self.performances[performance_id] = (user_id, path_to_file)
		self.main_queue.append(performance_id)
		self.users[user_id].queue.append(performance_id)
		return performance_id		

	def next_performance(self):
		if len(self.main_queue) > 0:
			performance_id = self.main_queue.popleft()
			performance = self.performances[performance_id]
			del self.performances[performance_id]
			self.current_performance = performance
			return performance
		return None


	def remove_performance(self, performance_id):
		if performance_id in self.performances:
			self.main_queue.remove(performance_id)
			del self.performances[performance_id]
		

	def list_all_performances(self):
		snapshot = []
		for performance_id in self.main_queue:
			user_id, path_to_file = self.performances[performance_id]
			snapshot.append((self.users[user_id].nickname, path_to_file))
		return snapshot


	def list_user_performances(self, user_id):
		if user_id not in self.users:
			return []

		snapshot = []
		for performance_id in self.users[user_id].queue:
			if performance_id in self.performances:
				snapshot.append(self.performances[performance_id])
		return snapshot


	def create_user(self, nickname):
		id = str(uuid.uuid4())
		user = User(id, nickname)
		self.users[id] = user
		return id


	def remove_user(self, user_id):
		if user_id in self.users:
			#first remove all performances for a given user
			user = self.users[user_id]
			if len(user.queue) > 0:
				for performance_id in user.queue:
					self.remove_performance(performance_id)
		
			#then remove user
			del self.users[user_id]


	def list_all_users(self):
		snapshot = []
		for user in self.users.values():
			snapshot.append(user)
		return snapshot

	def clear_users(self):
		self.users = dict()


class User(object):
	"""docstring for User"""
	def __init__(self, id, nickname):
		self.id = id
		self.nickname = nickname
		self.queue = deque() #performance_id

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return '{\"id\":\"%s\", \"nickname\":\"%s\"}' % (self.id, self.nickname)


def main():

	#test here
	store = KaraokeStore()
	
	#create users
	ralph_id = store.create_user("Ralph")
	jim_id = store.create_user("Jim")
	ronnie_id = store.create_user("Ronnie")
	lynda_id = store.create_user("Lynda")

	store.queue_perfomance(ralph_id, '/files/white wedding.mp3')
	store.queue_perfomance(jim_id, '/files/abc.mp3')
	abba_performance = store.queue_perfomance(lynda_id, '/files/abba.mp3')
	store.queue_perfomance(ralph_id, '/files/break on through.mp3')

	print "list all****"
	for s, v in store.list_all_performances():
		print s, v

	print "list user ralph****"
	for s, v in store.list_user_performances(ralph_id):
		print s, v

	print "remove performance***"
	store.remove_performance(abba_performance)

	print "list all****"
	for s, v in store.list_all_performances():
		print s, v

	print "list users***"
	for u in store.list_all_users():
		print u

if __name__ == '__main__':
	main()



		




