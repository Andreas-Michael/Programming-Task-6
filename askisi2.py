import random
import matplotlib as plt


class Oscilator(object):
    def __init__(self):
        self.on = False
        self.next = False
        self.timer = 0
    
delta = 6
p = 0.4
S = 2
cols = 20
rows = 50
oscs = [[Oscilator() for j in range(cols)] for i in range(rows)]
x = [-1,  0,  1, -1, 1, -1, 0, 1]
y = [-1, -1, -1,  0, 0,  1, 1, 1]
ons = []

for delta in range(2, 6):
        for p in range(0.2, 0.6, 0.1):
                for S in range(2, 6):
                        timer = 0
                        timer_arr = []
                        while timer < 60:
                        count = 0
                        for i in range(rows):
                                for j in range(cols):
                                    o = oscs[i][j]
                                    if o.on:
                                    count = count + 1
                                    if o.timer > 0:
                                        o.timer = o.timer - 1
                                    else:
                                            o.next = False
                                        else:
                                    adjacents = 0
                                        for k in range(len(x)):
                                        if i+x[k] > -1 and i+x[k] < rows and j+y[k] > -1 and j+y[k] < cols:
                                                if oscs[i+x[k]][j+y[k]].on:
                                                adjacents = adjacents + 1
                                        if adjacents < S and random.random() <= p:
                                            oscs[i][j].next = True
    
                        for i in range(rows):
                            for j in range(cols):
                                o = oscs[i][j]
                                    if o.on != o.next:
                                    o.on = o.next
                        ons.append(count)
                        timer_arr.append(timer)
                        timer = timer + 1
    
                        plt.xlabel('time')
                        plt.ylabel('Oscilators on')
                        plt.plot(timer_arr, ons, label = 'Oscilators on')
                        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
                        plt.suptitle('delta=%d, p=%0.1f, S=%d' % (delta, p, S))

                        for i in range(rows):
                        for j in range(cols):
                                oscs[i][j].on = False
                                oscs[i][j].next = False
                                oscs[i][j].timer = 0
