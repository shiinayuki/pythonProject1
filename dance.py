# -*- coding: UTF-8 -*-
import sys
import signal
import threading
import qi


def signal_handler(sig, frame):
    print('\n\nAborting.')
    if len(LauncherList) >= 1:
        for l in LauncherList:
            l.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


class Launcher(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)

        self.ready = False

        try:
            self.event = args[0]
            self.ip = args[1]
            self.behavior = args[2]

            self.session = qi.Session()
            self.session.connect("tcp://%s:9559" % self.ip)

        except Exception as e:
            raise e

        try:
            self.bh = self.session.service("ALBehaviorManager")
            self.tts = self.session.service("ALTextToSpeech")

            self.bh.stopAllBehaviors()
            if self.bh.isBehaviorInstalled(self.behavior) and self.bh.preloadBehavior(self.behavior):
                # self.tts.say("Ladies and gentlemen, we are getting ready!")
                print("%s ready for %s" % (self.ip, self.behavior))
                self.ready = True
            else:
                self.tts.say("Sorry, I can't start %s" % self.behavior)
                print("%s not installed on %s" % (self.behavior, self.ip))
                self.ready = False
        except Exception as e:
            self.ready = False
            print("can't contact %s" % self.ip)
            raise e

    def run(self):
        if self.ready:
            self.event.wait()
            print("%s starting" % self.ip)
            try:
                self.bh.startBehavior(self.behavior)
                print("%s started" % self.ip)
            except Exception as e:
                raise e


# This dictionary works like that : {IP_ADRESS_STRING : BEHAVIOR_NAME_STRING}
IPs_behaviors_dict = {
   # "192.168.31.44": "nao-1-0c10a4",
    #"192.168.31.120": "nao-1-0c10a4",
    #"192.168.31.32": "nao-1-0c10a4",
    # "192.168.31.132": "nao-1-0c10a4",
    # "192.168.31.206": "nao-1-0c10a4"
}
LauncherList = []

event = threading.Event()

for ip, behavior in IPs_behaviors_dict.iteritems():
    print (ip)
    LauncherList.append(Launcher(args=(event, ip, behavior)))

for launcher in LauncherList:
    launcher.start()

i = 0
while i != len(LauncherList):
    for launcher in LauncherList:
        if launcher.ready:
            i += 1
raw_input("fire_event pressing enter")
event.set()
# -*- coding: UTF-8 -*-
import sys
import signal
import threading
import qi


def signal_handler(sig, frame):
    print('\n\nAborting.')
    if len(LauncherList) >= 1:
        for l in LauncherList:
            l.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


class Launcher(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)

        self.ready = False

        try:
            self.event = args[0]
            self.ip = args[1]
            self.behavior = args[2]

            self.session = qi.Session()
            self.session.connect("tcp://%s:9559" % self.ip)

        except Exception as e:
            raise e

        try:
            self.bh = self.session.service("ALBehaviorManager")
            self.tts = self.session.service("ALTextToSpeech")

            self.bh.stopAllBehaviors()
            if self.bh.isBehaviorInstalled(self.behavior) and self.bh.preloadBehavior(self.behavior):
                # self.tts.say("Ladies and gentlemen, we are getting ready!")
                print("%s ready for %s" % (self.ip, self.behavior))
                self.ready = True
            else:
                self.tts.say("Sorry, I can't start %s" % self.behavior)
                print("%s not installed on %s" % (self.behavior, self.ip))
                self.ready = False
        except Exception as e:
            self.ready = False
            print("can't contact %s" % self.ip)
            raise e

    def run(self):
        if self.ready:
            self.event.wait()
            print("%s starting" % self.ip)
            try:
                self.bh.startBehavior(self.behavior)
                print("%s started" % self.ip)
            except Exception as e:
                raise e


# This dictionary works like that : {IP_ADRESS_STRING : BEHAVIOR_NAME_STRING}
IPs_behaviors_dict = {
    "192.168.31.44": "nao-1-0c10a4",
    "192.168.31.120": "nao-1-0c10a4",
    "192.168.31.32": "nao-1-0c10a4",
    # "192.168.31.132": "nao-1-0c10a4",
    # "192.168.31.206": "nao-1-0c10a4"
}
LauncherList = []

event = threading.Event()

for ip, behavior in IPs_behaviors_dict.iteritems():
    print (ip)
    LauncherList.append(Launcher(args=(event, ip, behavior)))

for launcher in LauncherList:
    launcher.start()

i = 0
while i != len(LauncherList):
    for launcher in LauncherList:
        if launcher.ready:
            i += 1
raw_input("fire_event pressing enter")
event.set()
