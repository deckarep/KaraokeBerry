#depends on the Command Line interface of VLC
#VLC Command Line interface must be enabled for these commands to work
#Open VLC
#Preferences
#Show All
#Interface -> Main Interface
#turn on Command Line (not RC (old))
#when VLC is started from command line you can type help to get a list of supported commands
import subprocess
import time

VLC_PATH = '/Applications/VLC.app/Contents/MacOS/VLC'

class Controller(object):
	'''VLC based controller'''
	
	def __init__(self):
		super(Controller, self).__init__()
		self.history = []
		self.controller_process = None

	def is_alive(self):
		return not(self.controller_process is None)

	def command(self, commandText):
		if self.is_alive():
			print "Issue command: %s" % commandText		
			stdoutdata, stderrdata = self.controller_process.communicate(input=commandText)
			print 'stdoutdata: %s' + stdoutdata
			print 'stderrdata: %s' + stderrdata

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
		self.command('pause')

	def play(self):
		self.command('play')

	def start(self, path_to_file):
		'''Plays a song immediatley whether or not one is already playing'''
		#opens in another process
		#self.controller_process = subprocess.Popen([VLC_PATH, ' --play-and-exit ', ' --fullscreen ', ' --video-on-top ', path_to_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.controller_process = subprocess.Popen([VLC_PATH, path_to_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)		
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
		self.controller_process.terminate()

def main():
	c = Controller()
	c.start('/Users/ralphcaraveo/Karaoke/LeAnn Rimes - How Do I Live.mp3')
	
	time.sleep(10)
	c.toggle_fullscreen()
	

if __name__ == '__main__':
	main()

