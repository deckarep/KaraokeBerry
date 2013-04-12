

#should redo virtualenv WITH site-packages so it sees the pykaraoke install
#*this worked!!!!

#python standard imports
import glob
import os
import subprocess

#flask specific imports
from flask import Flask, session, redirect, url_for, escape, request, jsonify

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
    songlist = ['robert', 'ronaldo', 'adrian', 'barbara', 'rick', 'chris', 'sierra', 'daniel', 'chrisanne', 'ruben', 'jeremy', 'john', 'jimmy', 'jackson', 'jonas', 'mycal', 'melinda', 'melissa', 'steve', 'steven', 'steffan', 'jack', 'sonia', 'ralph', 'nicole', 'sophia', 'ronnie', 'jesse', 'adrianna', 'mia', 'aviara'] 
    for token in songlist:
        if keyword in token:  
            resultlist.append("<strong>You've got the look</strong> - " + token)
    return jsonify(dict(songs=resultlist))
     

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


