import random
import constants

import pygaze
from pygaze import libscreen
from pygaze import libinput
from pygaze import libtime
from pygaze import eyetracker

from psychopy import visual

disp = libscreen.Display()
kb = libinput.Keyboard(timeout = None)
tracker = eyetracker.EyeTracker(disp)

fix = visual.Circle(pygaze.expdisplay,
                    size = 5,
                    lineWidth=10,
                    pos = [0, 0])

target = visual.Circle(pygaze.expdisplay,
                    size = 20,
                    fillColor=[-1,-1,-1],
                    lineColor=[0,0,0],
                    pos = [100, 200])
distractor = visual.Circle(pygaze.expdisplay,
                    size = 20,
                    fillColor=[1, 1, 1],
                    lineColor=[1, 1, 1],
                    pos = [200, 100])

dist = 0

fixscreen = libscreen.Screen()
fixscreen.screen.append(fix)

targetscreen = libscreen.Screen()
targetscreen.screen.append(target)
targetscreen.screen.append(fix)

distractorscreen = libscreen.Screen()
distractorscreen.screen.append(target)
distractorscreen.screen.append(distractor)
distractorscreen.screen.append(fix)

resultscreen = libscreen.Screen()

tracker.calibrate()

while True:
    print 'starting trial'

    tracker.fix_triggered_drift_correction((constants.DISPSIZE[0]/2, constants.DISPSIZE[1]/2),
                                           min_samples = 30,
                                           max_dev = 120,
                                           reset_threshold=20)
    tracker.start_recording()
    fix.lineColor = fix.fillColor = [1,1,1]
    disp.fill(fixscreen)
    disp.show()
    libtime.pause(1000)
    fix.lineColor = fix.fillColor = [-1,-1,-1]
    disp.fill(fixscreen)
    disp.show()
    libtime.pause(500)

    if random.random() < 0.5:
        target.pos = [100, 200]
        distractor.pos = [200, 100]
    else:
        target.pos = [200, 100]
        distractor.pos = [100, 200]

    if random.random() < 0.5:
        disp.fill(distractorscreen)
        dist = 1
    else:
        disp.fill(targetscreen)
        dist = 0
    disp.show()

    tracker.wait_for_fixation_end()
    disp.show()
    pos = tracker.wait_for_fixation_start()
    tracker.stop_recording()

    color = [1, 0, 0]
    if dist == 0:
        color = [0, 1, 0]
    print pos[1]
    npos = [pos[1][0] - constants.DISPSIZE[0]/2, constants.DISPSIZE[1]/2 - pos[1][1]]
    print npos
    landing = visual.Circle(pygaze.expdisplay,
                            pos = npos,
                            size = 10,
                            lineColor=color,
                            fillColor=[-1,-1,-1])
    resultscreen.screen.append(landing)
    disp.fill(resultscreen)
    disp.show()

    print 'ending trial'
    k,t = kb.get_key(flush=True)
    if k == 'q':
        print 'quitting...'
        break
