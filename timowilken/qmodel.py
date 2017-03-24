import pickle
import os
from random import randint
import sys

class Qnode:
    def __init__(self):
        self.visit = 1
        self.value = 0

class Qmodel:
    def __init__(self, filew, state):
        self.qdict = {}
        self.discount = 0.8
        self.t = 1
        self.target = open('data/dictionary_status.txt', 'w')
        self.f = filew


        if os.stat("data/qlearn.pkl").st_size == 0:
            self.qdict[(state, False)] = Qnode()
            self.qdict[(state, True)] = Qnode()
        else:
            print ('LOADED -- DICTIONARY VALUES: ')
            self.qdict = pickle.load(open('data/qlearn.pkl', 'rb'))



    def getAlpha(self, tuple):
        return 1/self.qdict[tuple].visit

    def getAction(self, state):
        fly_value = self.qdict[(state, True)].value
        drop_value = self.qdict[(state, False)].value

        random = randint(0, 100)
        num = (self.qdict[(state, True)].visit + self.qdict[(state, False)].visit) / 2
        if random < (75 + num / 20):
            return fly_value >= drop_value
        else:
            return not (fly_value >= drop_value)

    def V(self, state):
        if (state, False) not in self.qdict:
            self.qdict[(state, False)] = Qnode()
            self.target.seek(0)
            self.target.write(str(len(self.qdict)))
        if (state, True) not in self.qdict:
            self.target.seek(0)
            self.target.write(str(len(self.qdict)))
            self.qdict[(state, True)] = Qnode()

        maxv = max(self.qdict[(state, False)].value, self.qdict[(state, True)].value)
        # self.f.write(' maxV: {}, false: {}, true: {} \n'.format(maxv, self.qdict[(state, False)].value, self.qdict[(state, True)].value))
        return maxv

    def getQSample(self, new_state, reward):
        return reward + self.discount * self.V(new_state)

    def updateAction(self, old_tuple, new_state, reward):
        self.t += 1
        self.qdict[old_tuple].visit += 1
        self.qdict[old_tuple].value = self.qdict[old_tuple].value + self.getAlpha(old_tuple) * (self.getQSample(new_state, reward) - self.qdict[old_tuple].value)
        if (self.t == 70000):
            print ('***** SAVED DICTIONARY ******')
            self.t = 0
            pickle.dump(self.qdict, open('data/qlearn.pkl', 'wb'))
            sys.exit(0)

    def updateDeath(self, old_tuple, new_state, punishment):
        self.qdict[old_tuple].value = self.qdict[old_tuple].value + self.getAlpha(old_tuple) * (self.getQSample(new_state, punishment) - self.qdict[old_tuple].value)

    def writeValues(self, old_state, old_action, new_state, reward):
        self.f.write('s: {} \t action: {} \t t_value: {} \t f_value: {} \t new_s: {} \t reward: {}\n'.format(old_state, old_action, self.qdict[(old_state, True)].value, self.qdict[(old_state, False)].value, new_state, reward))

    def printValues(self, old_state, old_action, new_state, reward):
        print ('Old State: ', old_state, old_action)
        print ('  Q Value:', self.qdict[(old_state, old_action)].value)
        print ('  Q Visit:', self.qdict[(old_state, old_action)].visit)
        print ('  Action :', self.getAction(new_state))
        print ('  Reward :', reward)

        print ('-------------------------------------------------')
