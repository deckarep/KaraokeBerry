

#should redo virtualenv WITH site-packages so it sees the pykaraoke install
#*this worked!!!!

#python standard imports
import glob
import os
import subprocess
import time

#flask specific imports
from flask import Flask, session, redirect, url_for, escape, request, jsonify, Response

SONG_PATH = '/home/pi/'

pykaraoke_process = None

app = Flask(__name__)
app.debug = True
app.secret_key = 'Booga Time!' #secret session key more info at Flask documentation site

#static files test
@app.route("/mobile")
def mobile():
    return redirect(url_for('static', filename='index.html'))


@app.route("/")
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return "Hello World!, welcome to KaraokePi!"

@app.route("/songs")
def songs():
    files = glob.glob(os.path.join(SONG_PATH, '*.cdg'))
    return jsonify(dict(count=len(files), songs=files))

@app.route("/search/<keyword>")
def search(keyword):
    if keyword is not None:
        keyword = keyword.lower()
    resultlist = []
    songlist = [{'artist':'Lady Gaga', 'tracks':[{'t':'Poker Face','fp':'/home/pi/pokerface'}, {'t':'Bad Romance','fp':'/home/pi/badromance'}]},
		{'artist':'Billy Idol', 'tracks':[{'t':'White Wedding','fp':'/home/pi/whitewedding'}, {'t':'Eyes Without a Face','fp':'/home/pi/eyeswithoutface'}]},
		{'artist':'Adele', 'tracks':[{'t':'Skyfall','fp':'/home/pi/skyfall'}, {'t':'Rolling In the Deep','fp':'/home/pi/rollingdeep'}]}]
    for coll in songlist:
        if keyword in coll['artist'].lower():  
            resultlist.append(coll)
    return jsonify({'results':resultlist})
     

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post"><p><input type="text" name="username" /></p>
        <p><input type="submit" value="login" /></p></form>'''

#example of generator, this BLOCKS all other requests until finished NOTICE the sleep
#implies that Flask is single threaded by nature.
@app.route('/busy')
def busy_request():
    def generate():
        for x in xrange(10):
            yield x
            time.sleep(5)
    return Response(generate(), mimetype='text/html')
    

@app.route('/logout')
def logout():
    #remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/queue/<artist>")
def queue_artist(artist):
    return "TODO: queue_artist"

@app.route("/play/<artist>")
def play_artist(artist):
    #subprocess.call(['pykaraoke', os.path.join(SONG_PATH, 'pokerface.cdg')])
    global pykaraoke_process
    pykaraoke_process = subprocess.Popen(['pykaraoke', os.path.join(SONG_PATH, 'pokerface.cdg')])
    return "Now playing artist %s" % artist

@app.route("/stop/")
def stop_playing():
    if pykaraoke_process is not  None:
        pykaraoke_process.terminate()
    return "stopping subprocess"

if __name__ == "__main__":
    app.run('0.0.0.0')


