#!/opt/local/bin/python

import os,sys

import numpy as np

ALE_DIR = '/Users/john/proj/atari/tmp/ale_0.4.4/ale_0_4'

MOVES = '''
noop (0)
fire (1)
up (2)
right (3)
left (4)
down (5)
up-right (6)
up-left (7)
down-right (8)
down-left (9)
up-fire (10)
right-fire (11)
left-fire (12)
down-fire (13)
up-right-fire (14)
up-left-fire (15)
down-right-fire (16)
down-left-fire (17)
'''

OTHER_MOVES = '''
reset (40)
save-state (43)
load-state (44)
system-reset (45)
'''

def get_moves():
    xs = [x.strip() for x in MOVES.split('\n') if x.strip()]
    ans = {}
    noop = 18
    for x in xs:
        a,b = x.split()
        i = int(b.strip('()'))
        ans[a] = '%s,%s' % (i,noop)
    return ans

class Game(object):
    def __init__(self,game_name='breakout'):
        self.screen = None
        self.game_over = False
        self.score = 0
        xxx = os.system('%s/ale -disable_color_averaging true -run_length_encoding false -display_screen true -game_controller fifo_named %s/roms/%s.bin &' % (ALE_DIR,ALE_DIR,game_name))
        self._fin = open('./ale_fifo_out')
        self._fout = open('./ale_fifo_in','w')
        self.send('1,0,0,1')
        self.w,self.h = map(int,self.read().split('-'))
        self.move('1,18')
    def reset(self): self.send('45,45')
    def send(self,x):
        self._fout.write(x+'\n')
        self._fout.flush()
    def read(self): return self._fin.readline().strip()
    def move(self,move):
        self.send(move)
        self._fout.write(move+'\n')
        self._fout.flush()
        self._update()
        self._update()
    def _update(self):
        vals = [x.strip() for x in self.read().split(':')]
        assert(vals[-1]=='')
        x,y = vals[:-1]
        self.screen = x
        a,b = map(int,y.split(','))
        self.game_over = a==1
        self.score += b
        print self.score,self.game_over,y
    def play(self,moves_poss=None):
        import random
        if not moves_poss: moves_poss = get_moves().values()
        while not self.game_over:
            self.move(random.choice(moves_poss))
        #self.reset()
        self.end()
    def end(self):
        self._fin.close()
        self._fout.close()



