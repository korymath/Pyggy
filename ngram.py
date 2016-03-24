#wget http://cs.stanford.edu/people/karpathy/char-rnn/shakespeare_input.txt
# http://nbviewer.jupyter.org/gist/yoavg/d76121dfde2618422139

from collections import *
from random import random
from tqdm import tqdm

def generate_letter(lm, history, order):
        history = history[-order:]
        dist = lm[history]
        x = random()
        for c,v in dist:
            x = x - v
            if x <= 0: return c

def generate_text(lm, order, nletters=1000):
    history = '~' * order
    out = []
    for i in xrange(nletters):
        c = generate_letter(lm, history, order)
        history = history[-order:] + c
        out.append(c)
    return "".join(out)

def train_char_lm(fname, order=4):
    # data = file(fname).read()
    data = filter(None, open(fname, "r").read())
    lm = defaultdict(Counter)
    pad = '~' * order
    data = pad + data
    for i in tqdm(xrange(len(data)-order)):
        history, char = data[i:i+order], data[i+order]
        lm[history][char]+=1
    def normalize(counter):
        s = float(sum(counter.values()))
        return [(c,cnt/s) for c,cnt in counter.iteritems()]
    outlm = {hist:normalize(chars) for hist, chars in lm.iteritems()}
    return outlm

# lm = train_char_lm("sonnets.txt", order=6)

# print generate_text(lm, 6, nletters=200)