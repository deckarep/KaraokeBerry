

#should redo virtualenv WITH site-packages so it sees the pykaraoke install
#*this worked!!!!

#python standard imports
import glob
import os
from subprocess import call

#flask specific imports
from flask import Flask, session, redirect, url_for, escape, request, jsonify

SONG_PATH = '/home/pi/'

app = Flask(__name__)
app.debug = True
app.secret_key = 'Booga Time!' #secret session key more info at Flask documentation site

@app.route("/")
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return "Hello World!, welcome to KaraokePi!"

@app.route("/songs")
def songs():
   files = glob.glob(os.path.join(SONG_PATH, '*.cdg'))
   return jsonify(dict(count=len(files), songs=files))

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

@app.route("/play/<artist>")
def play_artist(artist):
    call(['pykaraoke', '/home/pi/pokerface.cdg'])
    return "Now playing artist %s" % artist


if __name__ == "__main__":
    app.run('0.0.0.0')


