import os
import sched
import gevent

import pycdg
from pykmanager import manager

POLL_AMOUNT = 1/6 #must be at least 100ms or less 1 second divided by 10

class Controller(object):
	'''PyKaraoke based controller'''
	
	def __init__(self, root_path = None):
		super(Controller, self).__init__()
		
		print 'init called'
		self.player = None		

		if root_path is None:
			self.ROOT_PATH = '/home/pi'
		else:
			self.ROOT_PATH = root_path

	def poll(self):
		while True:
			pycdg.manager.Poll()
			position = self.player.GetPos()
			if position == -1:
				self.player = None
				break
			gevent.sleep(POLL_AMOUNT)

	def is_alive(self):
		return (self.player is not None)

	def clear_playlist(self):
		pass

	def toggle_fullscreen(self):
		'''Toggles between fullscreen and regular'''
		pass

	def stop(self):
		'''Stops current stream from playing'''
		pass
		
	def toggle_pause(self):
		'''Toggles the state of the stream from paused to not paused'''
		if self.is_alive():
			self.player.Pause()

	def resume(self):
		pass

	def restart(self):
		'''Restart the current song'''
		pass

	def play_file(self, path_to_file):
		pass

	def enqueue_file(self, path_to_file):
		pass

	def next_track(self):
		pass

	def prev_track(self):
		pass

	def start(self, path_to_file = None):
		'''Plays a song immediatley whether or not one is already playing'''
		if path_to_file is None:
			pass
		else:
			fp = os.path.join(self.ROOT_PATH, path_to_file)
			self.player = pycdg.cdgPlayer(fp, None)
			self.player.Play()
			self.green_thread = gevent.spawn(self.poll)

	def is_playing(self):
		'''Indicates whether or not vlc is in the middle of a stream'''
		pass

	def stream_length(self):
		'''Return the length of the stream remaining'''
		pass

	def quit(self):
		'''Terminates the player instance'''
		if self.is_alive():
			self.player.shutdown()
			self.player = None


def main():
	controller = Controller()
	controller.start('pokerface.cdg')

	#prevent immediate shutdown in test mode

	gevent.sleep(10)
	controller.toggle_pause()
	gevent.sleep(5)
	controller.toggle_pause()
	gevent.joinall([controller.green_thread])


if __name__ == '__main__':
	main()

