import pycdg

player = pycdg.cdgPlayer('pokerface.cdg', None)
player.Play()

POLL_AMOUNT = 1/10 #must be at least 100ms or less 1 second divided by 10


import sched, time
s = sched.scheduler(time.time, time.sleep)
def poll_cdg(sc): 
    pycdg.manager.Poll()
    sc.enter(POLL_AMOUNT, 1, poll_cdg, (sc,))

s.enter(POLL_AMOUNT, 1, poll_cdg, (s,))
s.run()

