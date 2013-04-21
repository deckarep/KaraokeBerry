import uuid
from collections import deque
import json

#in memory store

class UserNotDefinedException(Exception):
	def __init__(self, user_id):
		self.user_id = user_id
	def __str__(self):
		return repr(self.user_id)


class KaraokeStore(object):
	
	def __init__(self):
		self.users = dict()
		self.main_queue = deque()
		self.history_of_performances = [] #TODO: implement the performance history
		self.performances = dict()
		self.current_performance = None
	
	def add_perfomance(self, performance):
		if not performance.user_id in self.users:
			raise UserNotDefinedException(performance.user_id)

		self.performances[performance.performance_id] = performance
		self.main_queue.append(performance.performance_id)

	def next_performance(self):
		'''grabs the next performance from the queue to play the song'''
		if len(self.main_queue) > 0:
			id = self.main_queue.popleft()
			performance = self.performances[id]
			del self.performances[id]
			self.current_performance = performance
			return performance
		return None

	def remove_performance(self, performance_id):
		'''removes a given performance from the main queue'''
		self.main_queue.remove(performance_id)
		del self.performances[id]
		
	def clear_performances(self):
		self.main_queue = deque()
		self.performances = dict()

	def list_all_performances(self):
		snapshot = []
		for id in self.main_queue:
			snapshot.append(self.performances[id])
		return snapshot

	def create_user(self, nickname):
		id = str(uuid.uuid4())
		user = User(id, nickname)
		self.users[id] = user
		return id

	def remove_user(self, id):
		if id in self.users:
			del self.users[id]

	def list_all_users(self):
		snapshot = []
		for user in self.users.items():
			snapshot.append(user)
		return snapshot

	def clear_users(self):
		self.users = dict()


class User(object):
	"""docstring for User"""
	def __init__(self, id, nickname):
		self.id = id
		self.nickname = nickname

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return '{\"id\":\"%s\", \"nickname\":\"%s\"}' % (self.id, self.nickname)


class Performance(object):
	"""docstring for Performance"""
	def __init__(self, user_id, song):
		super(Performance, self).__init__()
		self.performance_id = str(uuid.uuid4())
		self.user_id = user_id
		self.song = song

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return '{\"performance_id\":\"%s\", \"user_id\":\"%s\", \"song\":%s}' % (self.performance_id, self.user_id, self.song)


class KaraokeTrack(object):
	"""docstring for Song"""
	def __init__(self, path, name, artist):
		self.path = path
		self.name = name
		self.artist = artist

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return '{\"name\":\"%s\", \"path\":\"%s\", \"artist\":\"%s\"}' % (self.name, self.path, self.artist)

def main():
	#test here
	store = KaraokeStore()
	
	#create users
	ralph_id = store.create_user("Ralph")
	jim_id = store.create_user("Jim")
	ronnie_id = store.create_user("Ronnie")
	lynda_id = store.create_user("Lynda")

	#create tracks
	trackA = KaraokeTrack("/files/a.mp3", "Prince", "Purple Rain")
	trackB = KaraokeTrack("/files/b.mp3", "Billy Idol", "Eyes without a Face")
	trackC = KaraokeTrack("/files/c.mp3", "The Doors", "Break On Through")
	trackD = KaraokeTrack("/files/d.mp3", "Deep Purple", "Smoke on the Water")

	#create performances
	performanceA = Performance(ralph_id, trackA)
	performanceB = Performance(lynda_id, trackD)
	performanceC = Performance(ronnie_id, trackB)
	
	#add performances
	store.add_perfomance(performanceA)
	store.add_perfomance(Performance(lynda_id, trackD))
	store.add_perfomance(Performance(ronnie_id, trackB))

	#list state of store
	#print store.list_all_users()
	print store.list_all_performances()

	store.next_performance()

	print store.list_all_performances()

	store.next_performance()

	#print store.list_all_performances()

	store.next_performance()

	#print store.list_all_performances()

	store.next_performance()

if __name__ == '__main__':
	main()



		




