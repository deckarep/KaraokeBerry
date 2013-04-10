

#should redo virtualenv WITH site-packages so it sees the pykaraoke install

from subprocess import call

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/play/<artist>")
def play_artist(artist):
    call(['pykaraoke', '/home/pi/pokerface.cdg'])
    return "Now playing artist %s" % artist


if __name__ == "__main__":
    app.run('0.0.0.0')


