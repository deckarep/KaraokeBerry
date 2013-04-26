#depends on the Command Line interface of VLC
#VLC Command Line interface must be enabled for these commands to work
#Open VLC
#Preferences
#Show All
#Interface -> Main Interface
#turn on Command Line (not RC (old))
#when VLC is started from command line you can type help to get a list of supported commands
import subprocess
import urllib2
import urllib
import time
import os

VLC_PATH = '/Applications/VLC.app/Contents/MacOS/VLC'


class Controller(object):
	'''VLC based controller'''
	
	def __init__(self, root_path = None):
		super(Controller, self).__init__()
		
		if root_path is None:
			self.ROOT_PATH = '/Users/ralphcaraveo/Karaoke/'
		else:
			self.ROOT_PATH = root_path

		self.history = []
		self.controller_process = None

	def is_alive(self):
		return not(self.controller_process is None)

	def command(self, commandText, path_to_file = None):
		if self.is_alive():
			if commandText == 'play':
				rc = 'pl_play'
			elif commandText == 'pause':
				rc = 'pl_pause'
			elif commandText == 'fullscreen':
				rc = 'fullscreen'
			elif commandText == 'stop':
				rc = 'pl_stop'
			elif commandText == 'previous':
				rc = 'pl_previous'
			elif commandText == 'next':
				rc = 'pl_next'
			elif commandText == 'empty':
				rc = 'pl_empty'
			elif commandText == 'playfile':
				rc = 'in_play'
			elif commandText == 'enqueuefile':
				rc = 'in_enqueue'
			else:
				print 'Unknown command!'
				return #unknown command	
			
			if path_to_file is None:
				urllib2.urlopen('http://localhost:8080/requests/status.xml?command=' + rc)
			else:
				uri = 'http://localhost:8080/requests/status.xml?command=%s&input=%s' % (rc, path_to_file)
				urllib2.urlopen(uri)

	def clear_playlist(self):
		self.command('empty')		

	def toggle_fullscreen(self):
		'''Toggles between fullscreen and regular'''
		self.command('fullscreen')

	def enqueue_song(self, path_to_file):
		'''Enqueue's a song to be played in the future'''
		pass

	def stop(self):
		'''Stops current stream from playing'''
		self.command('stop')
		
	def toggle_pause(self):
		'''Toggles the state of the stream from paused to not paused'''
		print 'pausing...'
		self.command('pause')

	def play(self):
		self.command('play')

	def play_file(self, path_to_file):
		f = urllib.quote('file://%s' % path_to_file)
		self.command('playfile', f)

	def enqueue_file(self, path_to_file):
		f = urllib.quote('file://%s' % path_to_file)
		self.command('enqueuefile', f)

	def next_track(self):
		self.command('next')

	def prev_track(self):
		self.command('previous')

	def start(self, path_to_file = None):
		'''Plays a song immediatley whether or not one is already playing'''
		#opens in another process
		if path_to_file is None:
			self.controller_process = subprocess.Popen([VLC_PATH])
			print 'Process started'		
		else:
			self.controller_process = subprocess.Popen([VLC_PATH, path_to_file])		
			self.history.append(path_to_file)        	
			print 'Process started with file: %s' % path_to_file

	def is_playing(self):
		'''Indicates whether or not vlc is in the middle of a stream'''
		pass

	def stream_length(self):
		'''Return the length of the stream remaining'''
		pass

	def quit(self):
		'''Terminates the player instance'''
		if self.isalive():
			self.stop()
			self.controller_process.kill() #maybe find a nicer way to shutdown .terminate() didn't work for me.
			self.controller_process = None

def main():
	c = Controller()
	c.start()
	
	time.sleep(5)
	f = os.path.join(c.ROOT_PATH, 'Sugar Ray - Fly.mp3')
	c.play_file(f)


	time.sleep(5)
	f = os.path.join(c.ROOT_PATH, 'Smash Mouth - Walkin On The Sun.mp3')
	print f
	c.play_file(f)

	time.sleep(5)
	c.prev_track()
	time.sleep(5)
	c.next_track()

	c.quit()
	

if __name__ == '__main__':
	main()

