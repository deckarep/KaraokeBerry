

#should redo virtualenv WITH site-packages so it sees the pykaraoke install
#*this worked!!!!

#gevent (i love this technology)
from gevent import monkey
monkey.patch_all()
#from gevent.wsgi import WSGIServer
from gevent.pywsgi import WSGIServer


#python standard imports
import glob
import os
import subprocess
import time

#flask specific imports
from flask import Flask, session, redirect, url_for, escape, request, jsonify, Response, stream_with_context

SONG_PATH = '/Users/ralphcaraveo/Karaoke'

karaokePlayerProcess = None

app = Flask(__name__)
app.debug = True
app.secret_key = 'Booga Time!' #secret session key more info at Flask documentation site

#user functionality
#this is safe, since we're using gevent
users = set()
@app.route("/adduser/<name>")
def adduser(name):
    users.add(name)
    return "User %s added" % name

@app.route("/deleteuser/<name>")
def removeuser(name):
    if name in users:
        users.remove(name)
        return "User %s removed" % name
    else:
        return "User %s not found." % name

@app.route("/clearusers")
def clearusers():
    users.clear()
    return "All users cleared"

@app.route("/showusers/")
def showusers():
    if len(users) == 0:
        return "none"
    else:
        return ", ".join(users)


#static files test
@app.route("/mobile")
def mobile():
    return redirect(url_for('static', filename='index.html'))


@app.route("/")
def index():
    return redirect(url_for("mobile"))
    # if 'username' in session:
    #     return 'Logged in as %s' % escape(session['username'])
    # return "Hello World!, welcome to KaraokePi!"

@app.route("/songs")
def songs():
    files = glob.glob(os.path.join(SONG_PATH, '*.cdg'))
    return jsonify(dict(count=len(files), songs=files))

def createFakeTrackList():
    # songlist = [
    #     {'artist':'Lady Gaga', 'tracks':[{'t':'Poker Face','fp':'/home/pi/pokerface', 'tid':000}, {'t':'Bad Romance','fp':'/home/pi/badromance', 'tid':001}]},
    #     {'artist':'Billy Idol', 'tracks':[{'t':'White Wedding','fp':'/home/pi/whitewedding', 'tid':002}, {'t':'Eyes Without a Face','fp':'/home/pi/eyeswithoutface', 'tid':003}]},
    #     {'artist':'Adele', 'tracks':[{'t':'Skyfall','fp':'/home/pi/skyfall', 'tid':004}, {'t':'Rolling In the Deep','fp':'/home/pi/rollingdeep', 'tid':005}]}
    # ]
    songlist = []
    files = glob.glob(os.path.join(SONG_PATH, '*.mp3'))

    for file_path in files:
        name = os.path.basename(file_path)
        artist, song = name.split('-')
        song = song.strip().replace('.mp3', '')
        artist = artist.strip()
        songlist.append(
            {'artist':artist, 'tracks':[{'t':song,'fp':name, 'tid':000}]}
        )
        print songlist
    return songlist

#TODO TODO TODO:WARNING - search routine below is doing a glob for every keypress, need to index ahead of time first
# create method to gen index.       

@app.route("/search/<keyword>")
def search(keyword):
    if keyword is not None:
        keyword = keyword.lower()
    resultlist = []
    songlist = createFakeTrackList()
    for coll in songlist:
        if keyword in coll['artist'].lower():  
            resultlist.append(coll)
    return jsonify({'results':resultlist})
     
@app.route('/piaddress')
def piaddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    result = s.getsockname()[0]
    s.close()
    return result

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post"><p><input type="text" name="username" /></p>
        <p><input type="submit" value="login" /></p></form>'''

@app.route('/logout')
def logout():
    #remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))        

#example of generator, this BLOCKS all other requests until finished NOTICE the sleep
#implies that Flask is single threaded by nature.
#with gevent this is working while yielding to other requests (Excellent!)
@app.route('/busy')
def busy_request():
    def generate():
        for x in xrange(10):
            yield "Hello"
            time.sleep(1)
    return Response(generate(), mimetype='text/event-stream', direct_passthrough=True)

#alternative from Flask documentation
@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        time.sleep(1)
        yield 'Hi'
        time.sleep(5)
        yield '!'
    return Response(stream_with_context(generate()))    
    
@app.route("/queue/<artist>")
def queue_artist(artist):
    return "TODO: queue_artist"

@app.route("/play/<artist>")
def play_artist(artist):
    path = os.path.join(SONG_PATH, artist)
    #example using subprocess DON'T USE
    #subprocess.call(['pykaraoke', os.path.join(SONG_PATH, 'pokerface.cdg')])  #blocks and waits
    
    global karaokePlayerProcess
    
    #using pykaraoke
    #karaokePlayerProcess = subprocess.Popen(['pykaraoke', os.path.join(SONG_PATH, 'pokerface.cdg')])  #opens in another process
    
    #using vlc
    if karaokePlayerProcess is None:
        karaokePlayerProcess = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', '--fullscreen', '--play-and-exit', '--video-on-top', '--video-on-top', path])  #opens in another process
        verbose = "Now playing file: %s" % artist
        return jsonify(dict(result="OK", verbose=verbose))

@app.route("/pause")
def pause_player():
    pass
    #subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', '--fullscreen', '--play-and-exit', '--video-on-top', '--video-on-top', path])  #opens in another process

@app.route("/stop")
def stop_playing():
    subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', 'vlc://quit'])
    return "stopping vlc"
    # if karaokePlayerProcess is not None:
    #     karaokePlayerProcess.terminate()
    # return "stopping subprocess"

if __name__ == "__main__":
    http_server = WSGIServer(('', 5555), app)  #can i run gevent on raspberry pi?
    http_server.serve_forever()
    #flask style
    #app.run('0.0.0.0', port=5555)


