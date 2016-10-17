#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *** MORPHED IDENTIFICATION TASK ****
#https://gist.github.com/JoshGlue/8cc6b60a65b039f864462b47fef19db7
# Two alternative forced choice task with morphed (11 steps) stimuli

# import necessary libraries
from psychopy import core, visual, event, sound, gui, logging, data
import csv       # for output writer
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions


# setup pop-up window: define participant's ID, counter and day of training
expName = 'Auditory Tonal Difference'
expInfo = {'participant':'' , 
'Man/Vrouw' : ['Man', 'Vrouw'], 
'Leeftijd': '',
'Heb je gehoorproblemen?': ['Nee', 'Ja'], 
 'Speel je een muziekinstrument?': ['Nee', 'Ja'],
 'Kan je een Limburgs dialect spreken?': ['Nee', 'Ja']
 }
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
    
# add info to info array
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

gender = expInfo['Man/Vrouw']
age = expInfo['Leeftijd']
hearing_impairment = expInfo['Heb je gehoorproblemen?']
playing_music = expInfo['Speel je een muziekinstrument?']
limburgian_dialect = expInfo['Kan je een Limburgs dialect spreken?']
#------------- VARIABLES -----------------------

#win = visual.Window([700,500], monitor="testMonitor", units="cm", fullscr=False)
win = visual.Window([1280, 800], monitor="testMonitor", fullscr=True)

# extract variables from pop-up window (all strings!)
counter = '1'      
participantID = expInfo['participant']
day = '1'
date = expInfo['date']


# stim words
stim1 = 'asa1343'
# create stim list with elements from 2 - 9 (50% of stimuli)
stim = []
for i in range(2,10):
    stim.append(str(i))
# extend stim list with element 1 (50% of stimuli)
totalstim = len(stim)
for i in range(totalstim):
	stim.append('1')
print stim

# n of repetitions for the minimal unit (ntrials equals nrep * minimal unit)
nRep = 5
nTrials = nRep*len(stim)

# create random sequence with STIM selection for all trials
stimSelect = []
for j in range(nRep):
    for i in range(len(stim)):
            stimSelect.append(stim[i])

shuffle(stimSelect)
print stimSelect
print len(stimSelect)


# select choice message and its order (counterbalanced - based on pop-up prescreen definition)
if counter == '1':
    choiceMessage = "{}                        {}".format('Hetzelfde', 'Verschillend')
elif counter == '2':
    choiceMessage = "{}                        {}".format('Verschillend', 'Hetzelfde')
else:
    print 'choice message not attributed - counterbalance wrong'
message = visual.TextStim(win, alignHoriz="center", text=choiceMessage)


# fixation cross (maybe not needed after all; seems overproportionalised in full screen mode...)
fixation = visual.ShapeStim(win,
    vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
    lineWidth=5,
    closeShape=False,
    lineColor='white')

# instructions
#instr_welcome = 'Welcome to the Task'
#instr_1 = 'Please focus on the fixation cross. You are gonna hear sounds.... Please indicate which of the two displayed words your heard last'
#instr_end = 'This is the end of the task.\n Thank you for participating!'
instr_welcome = visual.TextStim(win, text='Welkom bij dit onderzoek.')

instr_1 = visual.TextStim(win, text='Je krijgt twee geluidsfragmenten te horen waar "asa" wordt gezegd.'+
            ' Aan jou de taak om te kijken of jij het verschil kunt horen tussen beide geluidsfragmenten.'+
            ' Of er een verschil is, is af en toe moeilijk te horen, aarzel niet te lang en ga op je intuitie af.'+
            '\n'+
            'Het zal ongeveer 3 minuten duren.\n'+
            '\n'+
            'Heb je nog vragen? Zo niet, dan kan je op de rechterpijl klikken om te beginnen. Succes!')
instr_end = visual.TextStim(win, text = 'This is the end of the task.\n Thank you for participating!')



# ----------------- useful FUNCTIONS -------------------

def showText(window, inputText="Text"):
    message = visual.TextStim(window, alignHoriz="center", text=inputText)
    message.draw()
    window.flip()





 ############################### EXPERIMENT running ##############################

# welcome instructions
instr_welcome.draw()
win.flip()
event.waitKeys(keyList = ['left', 'right'])

# task instructions
instr_1.draw()
win.flip()
event.waitKeys(keyList = ['left', 'right'])

showText(win, '')       # blank
core.wait(0.5)

# open/ create outputfile
backgroundinfo= open("data/{}_{}_{}_limburgiantonaldifference_backgroundinfo.csv".format(participantID, day, date), 'wb')
writer_background = csv.writer(backgroundinfo, delimiter=";")
writer_background.writerow(['gender', 'age', 'hearing_impairment',' playing_music', 'limburgian_dialect'])
writer_background.writerow([gender, age, hearing_impairment,playing_music,limburgian_dialect])
backgroundinfo.close()

outputfile= open("data/{}_{}_{}_OUTPUT_limburgiantonaldifference.csv".format(participantID, day, date), 'wb')
writer = csv.writer(outputfile, delimiter=";")
writer.writerow(['trial', 'stim', 't_soundPlay',' t_choice', 't_Response', 'RT', 'responseButton', 'Same', 'Different'])


timer = core.Clock()

for i in range(len(stimSelect)):
#for i in range(5):      # for test-run
    # timing
    timer.reset()
    s0 = sound.Sound(value = stim1 + '_1.wav', secs = 1)

    # load/prepare audio (secs is expected length but will not determine actual length? - see core.wait below)
    s = sound.Sound(value = stim1 + '_' + stimSelect[i] + '.wav' , secs = 1)
    
    # fixation cross
    showText(win, '')
#        fixation.draw()
#        win.flip()
    # start audio
    s0.play()
    core.wait(1)
    s.play()
    t_soundOnset = timer.getTime()
    soundDuration = s.getDuration()
    core.wait(soundDuration)

    # display choice message & fixation cross
    message.draw()
    showText(win, '')
#        fixation.draw()
#        win.flip()
    
    # get time and response
    t_choice = timer.getTime()
    buttonPressed = event.waitKeys(keyList = ['left', 'right'])
    t_response = timer.getTime()
    
    # display fix cross as delay
    showText(win, '')
#        fixation.draw()
#        win.flip()
    core.wait(0.5)
    
    # answer check (VAT or VET)
    VAT, VET = 0,0
    if counter=='1':  # determines the position of the two options for response, e.g. 'fan' left or write of fix  
        if buttonPressed == ['left']:
            print 'response: Hetzelfde'
            VAT = 1
        elif buttonPressed == ['right']:
            print 'response: Verschillend'
            VET = 1
        else:
            print 'wrong response'
    elif counter=='2':
        if buttonPressed == ['left']:
            print 'response: Verschillend'
            VET = 1
        elif buttonPressed == ['right']:
            print 'response: Hetzelfde'
            VAT = 1
        else:
            print 'wrong response'
    else:
        print 'COUNTER was not defined correctly'    

    # write in output file every trial
    RT = t_response - t_choice
    # header: 'trial', 'stim', 'counterChoice (1/2)', 't_soundPlay',' t_choice', 't_Response', 'RT', 'responseButton', 'VAT_classified', ' VET_classified'])
    writer.writerow([i+1, stimSelect[i],  
                    str(round(t_soundOnset, 3)), str(round(t_choice,3)), str(round(t_response,3)),
                    str(round(RT,3)), buttonPressed, VAT, VET
                    ])
    
    
    
    # check for quit (the Esc key)
    if event.getKeys(keyList=["escape"]):
        # close output
        outputfile.close()
        win.close()
        core.quit()
        

# close output file properly
outputfile.close()

# end instructions
instr_end.draw()
win.flip()

event.waitKeys()

# closing section
win.close()
core.quit()
