#depends on the Command Line interface of VLC
#VLC Command Line interface must be enabled for these commands to work
#Open VLC
#Preferences
#Show All
#Interface -> Main Interface
#turn on Command Line (not RC (old))
#when VLC is started from command line you can type help to get a list of supported commands
import subprocess

VLC_PATH = '/Applications/VLC.app/Contents/MacOS/VLC'

class Controller(object):
	'''VLC based controller'''
	
	def __init__(self):
		super(Controller, self).__init__()
		self.history = []
		self.controller_process = None

	def is_alive(self):
		return not(self.controller_process is None)

	def toggle_fullscreen(self):
		'''Toggles between fullscreen and regular'''
		pass

	def enqueue_song(self, path_to_file):
		'''Enqueue's a song to be played in the future'''
		pass

	def stop(self):
		'''Stops current stream from playing'''
		if self.is_alive():
			(stdoutdata, stderrdata) = self.controller_process.communicate('stop\n')
		

	def toggle_pause(self):
		'''Toggles the state of the stream from paused to not paused'''
		pass

	def play(self, path_to_file):
		'''Plays a song immediatley whether or not one is already playing'''
		#opens in another process
		if self.controller_process is None:
			self.controller_process = subprocess.Popen([VLC_PATH, '--fullscreen', '--play-and-exit', '--video-on-top', '--video-on-top', path_to_file], stdin=subprocess.PIPE)

		self.history.append(path_to_file)        	

	def is_playing(self):
		'''Indicates whether or not vlc is in the middle of a stream'''
		pass

	def stream_length(self):
		'''Return the length of the stream remaining'''
		pass

	def quit(self):
		'''Terminates the player instance'''
		pass


