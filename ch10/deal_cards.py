import random

values = list(range(1, 11)) + 'Jack Queen King'.split()
suits = 'diamonds clubs hearts spades'.split()
deck = ['{} of {}'.format(v, s) for v in values for s in suits]
random.shuffle(deck)
while deck:
    input(deck.pop() + '\n')
