# KaraokeBerry 0.1

Host a Karaoke party on your Raspberry Pi.

## What is KaraokeBerry?

A web-based app that will play Karaoke CDG/MP3 files using the HDMI output and audio output of the Raspberry Pi and allows for remote control through the use of one or more mobile devices.

## Is it ready?

The sytem is not yet completely built out to work on the Raspberry Pi.  All development has been done so far on a Mac running Mountain Lion.  It's currently working using a VLC remote controller that I built but I have to create one for the Raspberry Pi still.  This involves probably using PyKaraoke and somehow hooking into it so that it can be controlled remotely similar to how I'm doing it for VLC.

Also, the login system is not complete.  The searcher is slow, simply because I'm doing a naive linear O(n) search which is obviously not ideal.  I'll work on that eventually.

There is currently no persistence either.  If the system crashes, the state of app is lost.  Obviously not ideal.

## How it works

The idea is that you can take a regular Raspberry Pi running Raspbian and load it up with CDG/MP3 files of your choosing and with this software, host a Karaoke Party where the Pi is connected to your T.V. and your friends can log into the Pi with their mobile devices and browse the songs, add a song to their queue, favorite a song, and eventually get scored on their performances.  The host of the karaoke party can log into his/her device as an admin and manages the main queue of performances.  He/she can call up the next person, start the song, remove performances from the queue perhaps if someone leaves and manage a few other details.

Currently, all of this works within a users local lan.  None of the code calls out to the internet which means the Pi is not only playing the Karaoke tracks but also hosting the server-side component.

So please keep in mind, that with the Pi's limited hardware resources, you can't host a party that has 1000's of singers....but probably a small medium sized group is fine.  This is all speculation, I haven't benchmarked anything.

## Target Platforms

- OSX Mountain Lion (currently working)
- Raspberry Pi (not yet working)

## Where are the unit-tests? I don't use software that doesn't have unit-tests.

That's fine by me.  =)

## Software used

- Python (for the sweet, sweet language)
- Flask (for light-weight web application that hosts the Karaoke logic)
- Gevent (for coroutine, green threaded badass-ness)
- PyKaraoke (for playing Karaoke CDG/MP3 files on the Raspberry Pi)
- VLC Media Player (for playing Karaoke CDG/MP3 files on the VLC, only tested on Mac OSX 10.7)
- JQuery Mobile 1.3 (for mobile-web interfaces)
- Swipe.js (for mobile-web banners)

 
## Initial Setup

Everything below here needs to get formatted better)

From fresh install of Raspbian

    sudo apt-get update (installs latest OS)
    sudo apt-get install python-dev #required for gevent I believe
    sudo apt-get install libevent-dev #required for gevent for sure
    sudo apt-get install pip #required to install Python packages
    sudo apt-get install git-core #required to get the latest source via github.com
    sudo apt-get install pykaraoke (installs in main site-packages) #required to get the raspbian pykaraoke library
    
    source bin/activate (to activate your virtual-env)
    pip install flask
    pip install gevent

create a virtualenv (make sure that you are using site-packages otherwise can't reference pykaraoke)
7. go to Desktop
8. virtualenv KaraokePi
9. cd KaraokePi
10. source bin/activate
11. pip install flask
12. python KaraokeBerry.py (starts the Flask server)
13. consider using redis as a backing store, i see the light about redis being a kind of extension of Python with it's awesome datastructures

TODO:

1. run pykaraoke from a different child process
2. create whole rest api that's json based
3. create admin login so that only one admin can run the app
4. integrate jquery mobile site with flask server side backend (possibly due it all through rest requests with state simply in javascript local to the page???)
5. add the pi linux commands to this repository.
6. create admin interface that looks like windows metro blocks for pause, play, restart, fullscreen toggle, etc.

GETTING STARTED:
1. navigate to localhost:5000/mobile  (to see the jquery mobile interface in action)
2. read KaraokeBerry.py to see all the rest calls supported.

## About KaraokeBerry

KaraokeBerry actually exists in a previous incarnation as a simple C# .net Windows Forms app that I built for my wife years ago.  It basically
provided a simple GUI to search her karaoke library of music and with a double-click would launch WinAmp which had a CDG plugin that could
play the mp3 music and show the lyrics on the screen.  

We actually used it at a few Karaoke partys and I realized how much people love being able to digitally search a large library instead of
tediously combing over an out-dated printed book.

All of this was executed on a tiny netbook that was connected to my PA system (from my band days) and the netbook had a VGA out, that I connected
to a larger screen so people could sing along.

As time went by and mobile devices became more prevelant I realized that I needed to overhaul this thing and build it in a remote-controlled wireless
fashion with minimal hardware.  Since this is a one-man show KaraokeBerry is what I came up with.  This is my weekend warrior project and I 
finally found a good excuse to buy a Raspberry Pi and put the pieces together.

I could never take credit for this entire app because it obviously builds on some truly amazing open source software technologies.  I want to give 
a special shout-out to the Python Flask framework and to Gevent which is a mind-blowing tool for building highly responsive and scalable apps.

If you like Karaoke Berry please consider contributing and helping me make this software awesome.  I'm open to suggestions and I'm always looking
to improve my code and implementation details.

Feel free to fork this bad boy!

-Ralph [deckarep [at] gmail [dot] com]


